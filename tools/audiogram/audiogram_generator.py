#!/usr/bin/env python3
"""
Audiogram & Subtitle Sync Generator
===================================
A standalone tool to render Adobe-Podcast-style animated waveform bars
with frame-accurate synchronized karaoke subtitles, exporting either:
  1. Transparent video overlay (.mov ProRes 4444 / .webm VP9 alpha) to drop on any NLE editor.
  2. Solid-color composite video (.mp4) ready for social media / devlogs.
  3. Word-level timestamp JSON & SRT for custom player integrations.

Algorithm highlights:
  - 2048-point Hanning window FFT.
  - 46 log-spaced frequency bands (80 Hz to 8000 Hz, tuned for human voice & music).
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
    # 1. System PATH
    p = shutil.which("ffmpeg")
    if p:
        return p
    # 2. Common Antigravity / local paths
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


def compute_spectral_bands(pcm, sr, fps=30, num_bars=46):
    """
    Computes smoothed log-spaced frequency bands per video frame
    with silence gating, spatial neighborhood smoothing, and asymmetric decay.
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

    # Silence gate: collapse quiet background nubs to zero
    energies = raw.sum(axis=1)
    silence_thresh = np.percentile(energies, 10)
    lvl[energies < silence_thresh] *= 0.0

    # Spatial smoothing across neighboring bars
    k = np.array([0.15, 0.70, 0.15], dtype=np.float32)
    lvl = np.apply_along_axis(lambda r: np.convolve(r, k, mode="same"), 1, lvl)

    # Asymmetric temporal smoothing: fast attack (0.65), slower release (0.22)
    smoothed = np.zeros_like(lvl)
    for f in range(nframes):
        prev = smoothed[f - 1] if f > 0 else lvl[0]
        alpha = np.where(lvl[f] > prev, 0.65, 0.22)
        smoothed[f] = prev + alpha * (lvl[f] - prev)

    return smoothed, duration, nframes


def get_font(size, bold=False):
    font_paths = [
        "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/segoeuib.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf",
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


def transcribe_audio_whisper(audio_path, model_name="base"):
    """Runs local Whisper to obtain frame-accurate word-level timestamps."""
    try:
        import whisper
    except ImportError:
        print("[Notice] openai-whisper not installed. Skipping automatic speech transcription.")
        print("Install with: pip install openai-whisper")
        return []

    print(f">> Transcribing audio with local Whisper ({model_name})...")
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
    return words


def group_words_into_phrases(words, max_phrase_dur=3.0, max_words=6):
    """Groups individual word timestamps into human-readable phrase blocks."""
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
    active_word_color=(255, 255, 255, 255),
    inactive_word_color=(180, 180, 210, 200),
    author_text=None
):
    """Renders a single frame with rounded waveform bars and active-word highlighted subtitles."""
    img = Image.new("RGBA", (width, height), bg_color)
    draw = ImageDraw.Draw(img)

    # 1. Draw Waveform Bars
    num_bars = len(bars)
    # Total width allocated to bars = 80% of canvas width or fixed
    waveform_w = min(int(width * 0.85), 900)
    waveform_h = int(height * 0.28)
    start_x = (width - waveform_w) // 2
    base_y = height - 40

    slot_w = waveform_w / num_bars
    bar_w = max(4, int(slot_w * 0.55))

    for i, h_norm in enumerate(bars):
        bx = start_x + int(i * slot_w + (slot_w - bar_w) / 2)
        # Minimum baseline nub of 4px
        bh = max(6, int(h_norm * waveform_h))
        by = base_y - bh
        radius = bar_w // 2
        # Rounded-top vertical bar
        draw.rounded_rectangle([bx, by, bx + bar_w, base_y], radius=radius, fill=bar_color)

    # 2. Draw Synchronized Subtitles (if phrase is active)
    if phrase and phrase["start"] <= current_time <= phrase["end"] + 0.3:
        font_sub = get_font(38, bold=True)
        words = phrase["words"]
        
        # Calculate full line width
        word_widths = []
        space_w = draw.textlength(" ", font=font_sub)
        total_line_w = 0.0
        for w in words:
            wl = draw.textlength(w["word"], font=font_sub)
            word_widths.append(wl)
            total_line_w += wl + space_w
        total_line_w -= space_w

        text_x = (width - total_line_w) / 2
        text_y = height // 2 - 20

        # Draw speaker label if provided
        if author_text:
            font_author = get_font(20, bold=False)
            aw = draw.textlength(author_text, font=font_author)
            draw.text(((width - aw) / 2, text_y - 45), author_text, font=font_author, fill=(200, 200, 220, 220))

        # Draw each word with active karaoke highlight
        curr_x = text_x
        for i, w in enumerate(words):
            is_active = (w["start"] <= current_time <= w["end"] + 0.08)
            color = active_word_color if is_active else inactive_word_color
            draw.text((curr_x, text_y), w["word"], font=font_sub, fill=color)
            curr_x += word_widths[i] + space_w

    return img


def main():
    parser = argparse.ArgumentParser(description="Generate Adobe-Podcast-style audiogram with synchronized subtitles.")
    parser.add_argument("--audio", required=True, help="Input audio file (WAV, MP3, AAC, etc.)")
    parser.add_argument("--out", required=True, help="Output video file (.mov, .webm, or .mp4)")
    parser.add_argument("--format", choices=["transparent_mov", "transparent_webm", "solid_mp4"], default="solid_mp4",
                        help="Video export format: transparent overlay or standalone composite.")
    parser.add_argument("--width", type=int, default=1280, help="Canvas width (default: 1280)")
    parser.add_argument("--height", type=int, default=720, help="Canvas height (default: 720)")
    parser.add_argument("--fps", type=int, default=30, help="Video framerate (default: 30)")
    parser.add_argument("--bars", type=int, default=46, help="Number of frequency bands (default: 46)")
    parser.add_argument("--subtitles", action="store_true", help="Enable Whisper subtitle transcription & syncing.")
    parser.add_argument("--author", type=str, default="", help="Optional speaker name label displayed above subtitles.")
    parser.add_argument("--bg_color", type=str, default="5c24ff", help="Background hex color for solid_mp4 (default: 5c24ff purple).")
    parser.add_argument("--bar_color", type=str, default="ffffff", help="Bar hex color (default: ffffff white).")
    parser.add_argument("--whisper_model", type=str, default="base", help="Whisper model size (tiny, base, small).")
    parser.add_argument("--export_json", type=str, default=None, help="Optional output path to save word timestamps JSON.")
    args = parser.parse_args()

    ffmpeg = find_ffmpeg()
    print(f">> Using FFmpeg at: {ffmpeg}")

    # Parse colors
    def hex_to_rgba(h, alpha=255):
        h = h.lstrip("#")
        return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), alpha)

    if args.format.startswith("transparent"):
        bg_color = (0, 0, 0, 0)
    else:
        bg_color = hex_to_rgba(args.bg_color, alpha=255)

    bar_color = hex_to_rgba(args.bar_color, alpha=255)

    # 1. Load Audio
    print(f">> Decoding audio from {args.audio}...")
    pcm, sr = load_audio_pcm(args.audio, ffmpeg)

    # 2. Compute Waveform Bands
    print(f">> Computing {args.bars}-band log FFT with temporal smoothing...")
    spectral_levels, duration, nframes = compute_spectral_bands(pcm, sr, fps=args.fps, num_bars=args.bars)
    print(f"   Duration: {duration:.2f}s | Total frames: {nframes} @ {args.fps} FPS")

    # 3. Transcribe / Subtitle Alignment
    phrases = []
    if args.subtitles:
        words = transcribe_audio_whisper(args.audio, model_name=args.whisper_model)
        phrases = group_words_into_phrases(words)
        if args.export_json:
            with open(args.export_json, "w", encoding="utf-8") as f:
                json.dump({"words": words, "phrases": phrases}, f, indent=2)
            print(f"   Saved timestamp data to {args.export_json}")

    # 4. Setup Video Encoder Pipeline
    W, H = args.width, args.height
    
    if args.format == "transparent_mov":
        # Apple ProRes 4444 with alpha
        codec_flags = ["-c:v", "prores_ks", "-profile:v", "4444", "-pix_fmt", "yuva444p10le", "-alpha_bits", "16"]
    elif args.format == "transparent_webm":
        # VP9 with alpha
        codec_flags = ["-c:v", "libvpx-vp9", "-pix_fmt", "yuva420p", "-b:v", "1500k", "-auto-alt-ref", "0"]
    else:
        # Standard H.264 MP4 with input audio muxed
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

        # Find active phrase
        active_phrase = None
        if phrases:
            while curr_p_idx < len(phrases) - 1 and t > phrases[curr_p_idx]["end"] + 0.3:
                curr_p_idx += 1
            if curr_p_idx < len(phrases):
                active_phrase = phrases[curr_p_idx]

        img = render_audiogram_frame(
            W, H, bars, bar_color, bg_color,
            phrase=active_phrase, current_time=t,
            author_text=args.author if args.author else None
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
