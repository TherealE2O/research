/**
 * AudiogramVisualizer
 * ===================
 * Real-time 46-band log-spaced waveform visualizer using the HTML5 Web Audio API.
 * Replicates the Adobe Podcast audiogram algorithm in JavaScript for web & music player integration.
 * 
 * Features:
 *   - 2048 FFT with log-frequency band spacing (80 Hz to 8 kHz).
 *   - Voice/music tilt compensation.
 *   - Asymmetric temporal decay (fast attack, smooth release).
 *   - 3-tap spatial smoothing across adjacent bars.
 *   - Rounded-top bars rendered to HTML5 <canvas>.
 */
export class AudiogramVisualizer {
    constructor(canvas, options = {}) {
        this.canvas = canvas;
        this.ctx = canvas.getContext('2d');
        
        this.numBars = options.numBars || 46;
        this.barColor = options.barColor || '#ffffff';
        this.activeColor = options.activeColor || '#38bdf8';
        this.minBarHeight = options.minBarHeight || 6;
        this.fps = options.fps || 60;
        
        this.audioCtx = null;
        this.analyser = null;
        this.dataArray = null;
        this.smoothedLevels = new Float32Array(this.numBars);
        this.isRunning = false;

        // Precompute log-frequency band edges between 80 Hz and 8000 Hz
        this.bandIndices = [];
    }

    /**
     * Connects an existing HTML5 <audio> element to the Web Audio analyser.
     */
    connectAudioElement(audioElement) {
        if (!this.audioCtx) {
            const AudioContext = window.AudioContext || window.webkitAudioContext;
            this.audioCtx = new AudioContext();
        }
        
        if (this.audioCtx.state === 'suspended') {
            this.audioCtx.resume();
        }

        const source = this.audioCtx.createMediaElementSource(audioElement);
        this.analyser = this.audioCtx.createAnalyser();
        this.analyser.fftSize = 2048;
        this.analyser.smoothingTimeConstant = 0.2; // light hardware smoothing

        source.connect(this.analyser);
        this.analyser.connect(this.audioCtx.destination);

        const sampleRate = this.audioCtx.sampleRate;
        const binCount = this.analyser.frequencyBinCount;
        this.dataArray = new Uint8Array(binCount);

        // Precompute log-spaced bin ranges
        this.setupBands(sampleRate, binCount);
        this.startRenderLoop();
    }

    setupBands(sampleRate, binCount) {
        this.bandIndices = [];
        const minFreq = 80;
        const maxFreq = 8000;
        const freqPerBin = sampleRate / 2048;

        for (let i = 0; i < this.numBars; i++) {
            const fLow = minFreq * Math.pow(maxFreq / minFreq, i / this.numBars);
            const fHigh = minFreq * Math.pow(maxFreq / minFreq, (i + 1) / this.numBars);

            const bStart = Math.min(binCount - 1, Math.max(0, Math.floor(fLow / freqPerBin)));
            const bEnd = Math.min(binCount, Math.max(bStart + 1, Math.ceil(fHigh / freqPerBin)));

            this.bandIndices.push({ start: bStart, end: bEnd });
        }
    }

    startRenderLoop() {
        if (this.isRunning) return;
        this.isRunning = true;

        const render = () => {
            if (!this.isRunning) return;
            this.drawFrame();
            requestAnimationFrame(render);
        };
        requestAnimationFrame(render);
    }

    stop() {
        this.isRunning = false;
    }

    drawFrame() {
        const { width, height } = this.canvas;
        this.ctx.clearRect(0, 0, width, height);

        if (!this.analyser) {
            this.drawIdleBars();
            return;
        }

        this.analyser.getByteFrequencyData(this.dataArray);

        // Compute raw magnitude per log band with spectral tilt
        const raw = new Float32Array(this.numBars);
        for (let i = 0; i < this.numBars; i++) {
            const { start, end } = this.bandIndices[i];
            let sum = 0;
            for (let b = start; b < end; b++) {
                sum += this.dataArray[b];
            }
            const avg = sum / (end - start);
            const tilt = 1.0 - (i / this.numBars) * 0.18; // slight voice roll-off
            raw[i] = (avg / 255.0) * tilt;
        }

        // Spatial 3-tap convolution smoothing across neighbors
        const spatiallySmoothed = new Float32Array(this.numBars);
        for (let i = 0; i < this.numBars; i++) {
            const left = i > 0 ? raw[i - 1] : raw[i];
            const center = raw[i];
            const right = i < this.numBars - 1 ? raw[i + 1] : raw[i];
            spatiallySmoothed[i] = left * 0.15 + center * 0.70 + right * 0.15;
        }

        // Asymmetric temporal smoothing: fast attack (0.65), slower release (0.22)
        for (let i = 0; i < this.numBars; i++) {
            const target = spatiallySmoothed[i];
            const prev = this.smoothedLevels[i];
            const alpha = target > prev ? 0.65 : 0.22;
            this.smoothedLevels[i] = prev + alpha * (target - prev);
        }

        // Render Bars
        this.renderBars(this.smoothedLevels);
    }

    drawIdleBars() {
        // Draw baseline resting nubs when paused
        const idle = new Float32Array(this.numBars).fill(0.02);
        this.renderBars(idle);
    }

    renderBars(levels) {
        const { width, height } = this.canvas;
        const totalW = Math.min(width * 0.88, 900);
        const maxBarH = height * 0.75;
        const startX = (width - totalW) / 2;
        const baseY = height - 10;

        const slotW = totalW / this.numBars;
        const barW = Math.max(4, Math.floor(slotW * 0.58));

        this.ctx.fillStyle = this.barColor;

        for (let i = 0; i < this.numBars; i++) {
            const h = Math.max(this.minBarHeight, levels[i] * maxBarH);
            const x = startX + i * slotW + (slotW - barW) / 2;
            const y = baseY - h;
            const radius = barW / 2;

            // Draw rounded-top vertical bar
            this.ctx.beginPath();
            this.ctx.moveTo(x, baseY);
            this.ctx.lineTo(x, y + radius);
            this.ctx.arcTo(x, y, x + barW, y, radius);
            this.ctx.arcTo(x + barW, y, x + barW, y + radius, radius);
            this.ctx.lineTo(x + barW, baseY);
            this.ctx.closePath();
            this.ctx.fill();
        }
    }
}
