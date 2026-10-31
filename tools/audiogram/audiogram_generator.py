#!/usr/bin/env python3
"""
Audiogram & Whisper Subtitle Sync Generator
===========================================
A standalone tool to render Adobe-Podcast-style animated waveform bars
with frame-accurate synchronized karaoke subtitles driven by OpenAI Whisper.

Export options:
  1. Solid-color composite video (.mp4) with Whisper karaoke subtitles + 46-band waveform.
  2. Transparent video overlay (.mov ProRes 4444 / .webm VP9 alpha) to drop on any NLE editor.
  3. Word-level timestamp JSON & SRT for custom player integrations.

Algorithm highlights:
  - OpenAI Whisper word-level timestamp alignment (default: 'base' model).
  - Whisper-guided Voice Activity Gating (eliminates background hiss during pauses).
  - 2048-point Hanning window FFT across 46 log-spaced frequency bands (80 Hz to 8000 Hz).
  - Dynamic range contrast expansion & silence baseline gating.
  - Spatial 3-tap convolution smoothing across adjacent bars.
  - Asymmetric temporal smoothing: fast attack (0.65) + slower release (0.22).
  - Synchronized active-word highlight typography (karaoke pop effect).
"""

import argparse
import json
import math
import os
import shutil
import subprocess
import sys
import tempfile
import wave
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont


def find_ffmpeg():
    p = shutil.which("ffmpeg")
    if p:
        return p
    local_paths = [
        os.path.expanduser(r"~/.gemini/antigravity/bin/ffmpeg.exe"),
        os.path.expanduser(r"~/.gemini/antigravity/bin/ffmpeg"),
        r"C:\ffmpeg\bin\ffmpeg.exe",
    ]
    for lp in local_paths:
        if os.path.exists(lp):
            return lp
    return "ffmpeg"


def load_audio_pcm(audio_path, ffmpeg_bin):
    """Decode any audio format (WAV, MP3, AAC, FLAC) to 16kHz mono float32 PCM."""
    cmd = [
        ffmpeg_bin, "-v", "error", "-i", str(audio_path),
        "-f", "f32le", "-acodec", "pcm_f32le", "-ac", "1", "-ar", "16000", "pipe:1"
    ]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    raw, err = proc.communicate()
    if proc.returncode != 0:
        raise RuntimeError(f"FFmpeg audio decode failed: {err.decode('utf-8', errors='ignore')}")
    pcm = np.frombuffer(raw, dtype=np.float32)
    return pcm, 16000


def transcribe_audio_whisper(audio_path, model_name="base", precomputed_json=None):
    """
    Runs local OpenAI Whisper to obtain frame-accurate word-level timestamps.
    If precomputed_json is provided, loads existing alignment data directly.
    """
    if precomputed_json and os.path.exists(precomputed_json):
        print(f">> Loading precomputed Whisper timestamps from: {precomputed_json}")
        with open(precomputed_json, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, dict) and "words" in data:
                return data["words"], data.get("segments", [])
            elif isinstance(data, list):
                return data, []
            elif "segments" in data:
                words = []
                for s in data["segments"]:
                    for w in s.get("words", []):
                        words.append({
                            "word": w["word"].strip(),
                            "start": float(w["start"]),
                            "end": float(w["end"])
                        })
                return words, data["segments"]

    try:
        import whisper
    except ImportError:
        print("\n[Warning] 'openai-whisper' package is not installed.")
        print("To enable Whisper subtitle synchronization, run: pip install openai-whisper")
        return [], []

    print(f">> Transcribing audio with local OpenAI Whisper (model: '{model_name}')...")
    model = whisper.load_model(model_name)
    res = model.transcribe(str(audio_path), word_timestamps=True, fp16=False)
    
    words = []
    for seg in res.get("segments", []):
        for w in seg.get("words", []):
            words.append({
                "word": w["word"].strip(),
                "start": float(w["start"]),
                "end": float(w["end"])
            })
            
    print(f">> Whisper transcription complete: {len(words)} words aligned.")
    return words, res.get("segments", [])


def compute_spectral_bands(pcm, sr, fps=30, num_bars=46, whisper_words=None):
    """
    Computes smoothed log-spaced frequency bands per video frame
    with Whisper-assisted silence gating, spatial neighborhood smoothing, and asymmetric decay.
    """
    total_samples = len(pcm)
    duration = total_samples / sr
    nframes = int(math.ceil(duration * fps))

    N = 2048
    win = np.hanning(N).astype(np.float32)
    freqs = np.fft.rfftfreq(N, 1.0 / sr)
    edges = np.geomspace(80, 8000, num_bars + 1)
    
    band_idx = [np.where((freqs >= edges[i]) & (freqs < edges[i + 1]))[0] for i in range(num_bars)]
    for i, b in enumerate(band_idx):
        if len(b) == 0:
            band_idx[i] = np.array([np.argmin(np.abs(freqs - edges[i]))])
            
    tilt = np.linspace(1.0, 0.82, num_bars)

    pad = np.concatenate([np.zeros(N, np.float32), pcm, np.zeros(N, np.float32)])
    raw = np.zeros((nframes, num_bars), np.float32)

    for f in range(nframes):
        c = N + int((f + 0.5) / fps * sr)
        seg = pad[c - N // 2: c + N // 2] * win
        mag = np.abs(np.fft.rfft(seg))
        raw[f] = [mag[b].mean() for b in band_idx]

    raw *= tilt
    db = 20 * np.log10(raw + 1e-6)
    lo, hi = np.percentile(db, 50), np.percentile(db, 99.5)
    if hi - lo < 1e-3:
        hi = lo + 1.0
        
    lvl = np.clip((db - lo) / (hi - lo), 0, 1) ** 1.5

    # 1. Baseline Silence Gating
    energies = raw.sum(axis=1)
    silence_thresh = np.percentile(energies, 10)
    lvl[energies < silence_thresh] *= 0.0

    # 2. Whisper-Guided Voice Activity Gating:
    # Attenuates ambient noise in pauses between spoken words
    if whisper_words:
        in_speech = np.zeros(nframes, dtype=bool)
        for w in whisper_words:
            f_start = max(0, int((w["start"] - 0.15) * fps))
            f_end = min(nframes, int((w["end"] + 0.20) * fps))
            in_speech[f_start:f_end] = True
        
        for f in range(nframes):
            if not in_speech[f]:
                lvl[f] *= 0.15

    # 3. Spatial smoothing across neighboring bars
    k = np.array([0.15, 0.70, 0.15], dtype=np.float32)
    lvl = np.apply_along_axis(lambda r: np.convolve(r, k, mode="same"), 1, lvl)

    # 4. Asymmetric temporal smoothing: fast attack (0.65), slower release (0.22)
    smoothed = np.zeros_like(lvl)
    for f in range(nframes):
        prev = smoothed[f - 1] if f > 0 else lvl[0]
        alpha = np.where(lvl[f] > prev, 0.65, 0.22)
        smoothed[f] = prev + alpha * (lvl[f] - prev)

    return smoothed, duration, nframes


def get_font(size, bold=False):
    font_paths = [
        "C:/Windows/Fonts/segoeuib.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf",
        "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for fp in font_paths:
        if os.path.exists(fp):
            try:
                return ImageFont.truetype(fp, size)
            except Exception:
                pass
    return ImageFont.load_default()


def group_words_into_phrases(words, max_phrase_dur=3.2, max_words=7):
    """Groups individual Whisper word timestamps into natural subtitle phrase cards."""
    if not words:
        return []
    phrases = []
    curr = []
    for w in words:
        if not curr:
            curr.append(w)
            continue
        p_dur = w["end"] - curr[0]["start"]
        if len(curr) >= max_words or p_dur > max_phrase_dur:
            phrases.append({
                "start": curr[0]["start"],
                "end": curr[-1]["end"],
                "words": list(curr)
            })
            curr = [w]
        else:
            curr.append(w)
    if curr:
        phrases.append({
            "start": curr[0]["start"],
            "end": curr[-1]["end"],
            "words": list(curr)
        })
    return phrases


def render_audiogram_frame(
    width, height, bars, bar_color, bg_color,
    phrase=None, current_time=0.0,
    author_text=None, title_text=None, show_badge=True
):
    """Renders a single frame with header, rounded waveform bars, and active-word highlighted subtitles."""
    img = Image.new("RGBA", (width, height), bg_color)
    draw = ImageDraw.Draw(img)

    # 1. Header Elements (Title top-left, Badge top-right)
    if title_text:
        font_title = get_font(22, bold=True)
        draw.text((60, 48), title_text, font=font_title, fill=(255, 255, 255, 230))

    if show_badge and bg_color[3] > 0:  # Only on solid background
        font_badge = get_font(18, bold=True)
        badge_text = "🎙️ AUDIOGRAM"
        bw = draw.textlength(badge_text, font=font_badge)
        bx = width - bw - 75
        overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        odraw = ImageDraw.Draw(overlay)
        odraw.rounded_rectangle([bx - 14, 42, width - 50, 82], radius=10, fill=(255, 255, 255, 30), outline=(255, 255, 255, 80), width=1)
        odraw.text((bx, 50), badge_text, font=font_badge, fill=(255, 255, 255, 240))
        img = Image.alpha_composite(img, overlay)
        draw = ImageDraw.Draw(img)

    # 2. Draw Waveform Bars
    num_bars = len(bars)
    waveform_w = min(int(width * 0.85), 920)
    waveform_h = int(height * 0.28)
    start_x = (width - waveform_w) // 2
    base_y = height - 45

    slot_w = waveform_w / num_bars
    bar_w = max(4, int(slot_w * 0.55))

    for i, h_norm in enumerate(bars):
        bx = start_x + int(i * slot_w + (slot_w - bar_w) / 2)
        bh = max(6, int(h_norm * waveform_h))
        by = base_y - bh
        radius = bar_w // 2
        draw.rounded_rectangle([bx, by, bx + bar_w, base_y], radius=radius, fill=bar_color)

    # 3. Draw Synchronized Subtitles (if phrase is active)
    if phrase and phrase["start"] <= current_time <= phrase["end"] + 0.35:
        words = phrase["words"]
        font_reg = get_font(38, bold=False)
        font_bold = get_font(44, bold=True)
        text_y = height // 2 - 25

        # Draw speaker label if provided
        if author_text:
            font_author = get_font(20, bold=False)
            aw = draw.textlength(author_text, font=font_author)
            draw.text(((width - aw) / 2, text_y - 48), author_text, font=font_author, fill=(255, 255, 255, 175))

        # Precompute stable word slots so text layout does not shift or jitter when words bold up
        slot_data = []
        gap = 14
        for w in words:
            w_reg = draw.textlength(w["word"], font=font_reg)
            w_bold = draw.textlength(w["word"], font=font_bold)
            slot_w = max(w_reg, w_bold) + 4
            slot_data.append((slot_w, w_reg, w_bold))

        total_line_w = sum(s[0] for s in slot_data) + gap * (len(words) - 1)
        start_x = (width - total_line_w) / 2

        # Identify which word is active at current_time
        active_idx = None
        for i, w in enumerate(words):
            w_start = w["start"]
            w_end = min(w["end"] + 0.10, words[i + 1]["start"]) if i < len(words) - 1 else w["end"] + 0.12
            if w_start <= current_time <= w_end:
                active_idx = i
                break

        # Render frosted pill behind the active bold word
        if active_idx is not None:
            curr_x = start_x
            for i in range(active_idx):
                curr_x += slot_data[i][0] + gap
            slot_w, w_reg, w_bold = slot_data[active_idx]
            center_x = curr_x + slot_w / 2
            word_x = center_x - w_bold / 2
            word_y = text_y - 4  # Bolding UP: lifts 4px!

            pad_x = 12
            pad_y = 6
            pill_rect = [
                word_x - pad_x,
                word_y - pad_y,
                word_x + w_bold + pad_x,
                word_y + 44 + pad_y
            ]
            pill_overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))
            pdraw = ImageDraw.Draw(pill_overlay)
            pdraw.rounded_rectangle(
                pill_rect, radius=10,
                fill=(255, 255, 255, 45),
                outline=(255, 255, 255, 110),
                width=1
            )
            img = Image.alpha_composite(img, pill_overlay)
            draw = ImageDraw.Draw(img)

        # Draw each word
        curr_x = start_x
        for i, w in enumerate(words):
            slot_w, w_reg, w_bold = slot_data[i]
            center_x = curr_x + slot_w / 2

            if i == active_idx:
                # Active word bolds up with crisp stroke and lifted position
                word_x = center_x - w_bold / 2
                word_y = text_y - 4
                draw.text(
                    (word_x, word_y), w["word"],
                    font=font_bold,
                    fill=(255, 255, 255, 255),
                    stroke_width=1,
                    stroke_fill=(255, 255, 255, 255)
                )
            else:
                word_x = center_x - w_reg / 2
                word_y = text_y
                is_past = (current_time > w["end"] + 0.10)
                color = (255, 255, 255, 175) if is_past else (255, 255, 255, 105)
                draw.text((word_x, word_y), w["word"], font=font_reg, fill=color)

            curr_x += slot_w + gap

    return img


def export_srt_file(phrases, srt_path):
    """Exports synchronized phrases to standard SRT format."""
    def fmt_time(t):
        hrs = int(t // 3600)
        mins = int((t % 3600) // 60)
        secs = int(t % 60)
        ms = int(round((t - int(t)) * 1000))
        return f"{hrs:02d}:{mins:02d}:{secs:02d},{ms:03d}"

    with open(srt_path, "w", encoding="utf-8") as f:
        for idx, p in enumerate(phrases, 1):
            text = " ".join(w["word"] for w in p["words"])
            f.write(f"{idx}\n")
            f.write(f"{fmt_time(p['start'])} --> {fmt_time(p['end'])}\n")
            f.write(f"{text}\n\n")
    print(f">> Exported SRT subtitles to: {srt_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Audiogram Generator with Whisper Subtitle Synchronization."
    )
    parser.add_argument("--audio", required=True, help="Input audio file (WAV, MP3, AAC, FLAC).")
    parser.add_argument("--out", required=True, help="Output video file (.mov, .webm, or .mp4).")
    parser.add_argument("--format", choices=["solid_mp4", "transparent_mov", "transparent_webm"], default="solid_mp4",
                        help="Video export format (default: solid_mp4).")
    parser.add_argument("--width", type=int, default=1280, help="Canvas width (default: 1280).")
    parser.add_argument("--height", type=int, default=720, help="Canvas height (default: 720).")
    parser.add_argument("--fps", type=int, default=30, help="Video framerate (default: 30).")
    parser.add_argument("--bars", type=int, default=46, help="Number of frequency bands (default: 46).")
    
    # Whisper settings - Whisper is ON by default!
    parser.add_argument("--no_whisper", action="store_true", help="Disable Whisper subtitle transcription and render waveform only.")
    parser.add_argument("--whisper_model", type=str, default="base", help="Whisper model size: tiny, base, small, medium (default: base).")
    parser.add_argument("--whisper_json", type=str, default=None, help="Path to precomputed Whisper JSON to skip re-transcription.")
    
    parser.add_argument("--title", type=str, default="", help="Optional title displayed in top-left corner.")
    parser.add_argument("--author", type=str, default="", help="Optional speaker name displayed above subtitles.")
    parser.add_argument("--bg_color", type=str, default="5c24ff", help="Background hex color for solid_mp4 (default: 5c24ff purple).")
    parser.add_argument("--bar_color", type=str, default="ffffff", help="Bar hex color (default: ffffff white).")
    parser.add_argument("--export_srt", type=str, default=None, help="Optional path to save generated SRT subtitle file.")
    parser.add_argument("--export_json", type=str, default=None, help="Optional path to save word timestamps JSON.")
    args = parser.parse_args()

    ffmpeg = find_ffmpeg()
    print(f">> Using FFmpeg at: {ffmpeg}")

    def hex_to_rgba(h, alpha=255):
        h = h.lstrip("#")
        return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), alpha)

    if args.format.startswith("transparent"):
        bg_color = (0, 0, 0, 0)
    else:
        bg_color = hex_to_rgba(args.bg_color, alpha=255)

    bar_color = hex_to_rgba(args.bar_color, alpha=255)

    # 1. Load Audio
    print(f">> Decoding audio from: {args.audio}...")
    pcm, sr = load_audio_pcm(args.audio, ffmpeg)

    # 2. Whisper Speech Transcription & Alignment (Enabled by default)
    words = []
    phrases = []
    if not args.no_whisper:
        words, raw_segments = transcribe_audio_whisper(
            args.audio,
            model_name=args.whisper_model,
            precomputed_json=args.whisper_json
        )
        phrases = group_words_into_phrases(words)
        
        # Save SRT if requested
        if args.export_srt:
            export_srt_file(phrases, args.export_srt)
            
        # Save JSON if requested
        if args.export_json:
            with open(args.export_json, "w", encoding="utf-8") as f:
                json.dump({"words": words, "phrases": phrases}, f, indent=2)
            print(f">> Saved timestamp data to: {args.export_json}")
    else:
        print(">> Whisper subtitle syncing disabled by --no_whisper flag.")

    # 3. Compute Waveform Bands (with Whisper-guided voice activity gating)
    print(f">> Computing {args.bars}-band log FFT with temporal smoothing...")
    spectral_levels, duration, nframes = compute_spectral_bands(
        pcm, sr, fps=args.fps, num_bars=args.bars, whisper_words=words
    )
    print(f"   Duration: {duration:.2f}s | Total frames: {nframes} @ {args.fps} FPS")

    # 4. Setup Video Encoder Pipeline
    W, H = args.width, args.height
    
    if args.format == "transparent_mov":
        codec_flags = ["-c:v", "prores_ks", "-profile:v", "4444", "-pix_fmt", "yuva444p10le", "-alpha_bits", "16"]
    elif args.format == "transparent_webm":
        codec_flags = ["-c:v", "libvpx-vp9", "-pix_fmt", "yuva420p", "-b:v", "1500k", "-auto-alt-ref", "0"]
    else:
        codec_flags = ["-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p",
                       "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart"]

    enc_cmd = [
        ffmpeg, "-hide_banner", "-loglevel", "error", "-y",
        "-f", "rawvideo", "-pix_fmt", "rgba", "-s", f"{W}x{H}", "-r", str(args.fps),
        "-i", "-"
    ]
    if args.format == "solid_mp4":
        enc_cmd.extend(["-i", str(args.audio)])
        enc_cmd.extend(["-map", "0:v:0", "-map", "1:a:0", "-shortest"])
        
    enc_cmd.extend([*codec_flags, args.out])

    print(f">> Rendering frames to {args.out}...")
    pipe = subprocess.Popen(enc_cmd, stdin=subprocess.PIPE)

    curr_p_idx = 0
    for f in range(nframes):
        t = f / float(args.fps)
        bars = spectral_levels[f]

        active_phrase = None
        if phrases:
            while curr_p_idx < len(phrases) - 1 and t > phrases[curr_p_idx]["end"] + 0.35:
                curr_p_idx += 1
            if curr_p_idx < len(phrases):
                active_phrase = phrases[curr_p_idx]

        img = render_audiogram_frame(
            W, H, bars, bar_color, bg_color,
            phrase=active_phrase, current_time=t,
            author_text=args.author if args.author else None,
            title_text=args.title if args.title else None,
            show_badge=(args.format == "solid_mp4")
        )
        pipe.stdin.write(img.tobytes())

        if (f + 1) % (args.fps * 5) == 0 or f == nframes - 1:
            progress = (f + 1) / nframes * 100.0
            print(f"   Progress: {progress:5.1f}% ({f+1}/{nframes} frames)")

    pipe.stdin.close()
    pipe.wait()

    if pipe.returncode == 0:
        print(f"\n[Success] Output exported cleanly to: {args.out}")
    else:
        print(f"\n[Error] FFmpeg process exited with error code {pipe.returncode}")


if __name__ == "__main__":
    main()
