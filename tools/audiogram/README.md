# 🎙️ Audiogram & Subtitle Sync Toolkit

A high-performance, modular audio waveform visualizer and word-level synchronized subtitle engine inspired by Adobe Podcast Audiograms. 

Renders clean, rounded vertical frequency bars that pulse naturally to human speech or music beats, paired with karaoke-style active-word typography.

---

## 🌟 Features

- **46-Band Logarithmic FFT Waveform**: Spatially mapped from 80 Hz to 8,000 Hz across human vocal & musical formants.
- **Organic Motion Dynamics**:
  - **Asymmetric Temporal Smoothing**: Fast attack (0.65) so beats and syllables register instantly; gradual release (0.22) for smooth, floating decay.
  - **3-Tap Spatial Convolution**: Softens adjacent bars (`[0.15, 0.70, 0.15]`) creating cohesive rolling wave crests rather than jittery needles.
  - **Silence Gating**: Automatically collapses background noise to clean baseline resting nubs during speech pauses.
- **Synchronized Karaoke Subtitles**: Frame-accurate word-level alignment using local OpenAI Whisper (`base`, `tiny`, or `small`), with dynamic active-word luminance and scaling.
- **Multiple Video Export Pipelines**:
  - **Transparent Overlays**: ProRes 4444 (`.mov`, 16-bit alpha) or WebM VP9 (`.webm`, `yuva420p` alpha) ready to drag and drop over video editors (Premiere Pro, DaVinci Resolve, Final Cut, CapCut).
  - **Social Media Standalone**: Direct H.264 `.mp4` with custom brand background colors (e.g. Adobe purple `#5c24ff` or Slate `#0f172a`).
- **🎧 Music Player Ready**: Includes a zero-dependency HTML5 Web Audio API module (`audiogram_visualizer.js`) to plug directly into any web or mobile music player!

---

## 🚀 Quick Start (CLI)

### 1. Installation

```bash
git clone https://github.com/TherealE2O/research.git
cd research/tools/audiogram
pip install -r requirements.txt
```
*(Requires `ffmpeg` installed on your system PATH)*

### 2. Basic Standalone Video (with Subtitles)

```bash
python audiogram_generator.py \
    --audio sample.wav \
    --out my_audiogram.mp4 \
    --format solid_mp4 \
    --subtitles \
    --author "Speaker Name" \
    --bg_color 5c24ff
```

### 3. Transparent Video Overlay for Video Editors

Render an alpha-channel video strip to overlay on documentary footage or b-roll:

```bash
# ProRes 4444 (Mac / Premiere / DaVinci)
python audiogram_generator.py \
    --audio voiceover.wav \
    --out waveform_alpha.mov \
    --format transparent_mov \
    --bars 46

# WebM VP9 Alpha (Lightweight web & OBS overlay)
python audiogram_generator.py \
    --audio voiceover.wav \
    --out waveform_alpha.webm \
    --format transparent_webm
```

---

## 🎵 Music Player Integration (Web Audio API)

If you are building a web music player or audio app, you can use the exact same 46-band log visualizer in JavaScript:

```javascript
import { AudiogramVisualizer } from './web_player/audiogram_visualizer.js';

const canvas = document.getElementById('visualizerCanvas');
const audioEl = document.getElementById('musicPlayer');

// 1. Initialize Visualizer
const visualizer = new AudiogramVisualizer(canvas, {
    numBars: 46,
    barColor: '#ffffff',
    minBarHeight: 6
});

// 2. Connect to any HTML5 <audio> element
audioEl.onplay = () => visualizer.connectAudioElement(audioEl);
```

### 🌐 Interactive Web Demo
Open `web_player/index.html` in any modern browser to try the live player with custom audio file uploads or synthetic frequency sweeps!

---

## ⚙️ CLI Reference

| Flag | Default | Description |
| :--- | :--- | :--- |
| `--audio` | *(Required)* | Path to input audio file (WAV, MP3, AAC, FLAC). |
| `--out` | *(Required)* | Output video path (`.mp4`, `.mov`, `.webm`). |
| `--format` | `solid_mp4` | Export mode: `solid_mp4`, `transparent_mov`, `transparent_webm`. |
| `--bars` | `46` | Number of logarithmic frequency bars. |
| `--fps` | `30` | Video framerate. |
| `--subtitles` | `False` | Run local Whisper transcription and burn in synchronized subtitles. |
| `--whisper_model` | `base` | Whisper model size (`tiny`, `base`, `small`). |
| `--author` | `""` | Optional speaker tag displayed above subtitles. |
| `--bg_color` | `5c24ff` | Background hex color for solid composite videos. |
| `--bar_color` | `ffffff` | Waveform bar hex color. |
| `--export_json` | `None` | Optional path to export word-level timestamp JSON. |

---

## 📜 License
MIT License. Free to use in commercial and personal projects.
