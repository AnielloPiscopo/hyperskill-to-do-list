let audioContext: AudioContext | null = null

function getContext(): AudioContext {
    if (!audioContext) {
        audioContext = new AudioContext()
    }
    if (audioContext.state === 'suspended') {
        audioContext.resume()
    }
    return audioContext
}

export function playClickSound() {
    const ctx = getContext()

    const oscillator = ctx.createOscillator()
    const gain = ctx.createGain()

    oscillator.type = 'triangle'
    oscillator.frequency.setValueAtTime(520, ctx.currentTime)
    oscillator.frequency.exponentialRampToValueAtTime(660, ctx.currentTime + 0.04)

    gain.gain.setValueAtTime(0.001, ctx.currentTime)
    gain.gain.exponentialRampToValueAtTime(0.07, ctx.currentTime + 0.01)
    gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.12)

    oscillator.connect(gain)
    gain.connect(ctx.destination)

    oscillator.start(ctx.currentTime)
    oscillator.stop(ctx.currentTime + 0.12)
}

function clickSound(noiseFreq: number, blipFreq: number) {
    const ctx = getContext()

    const noiseDecay = 0.02
    const bufferSize = ctx.sampleRate * noiseDecay
    const buffer = ctx.createBuffer(1, bufferSize, ctx.sampleRate)
    const data = buffer.getChannelData(0)
    for (let i = 0; i < bufferSize; i++) {
        data[i] = (Math.random() * 2 - 1) * (1 - i / bufferSize)
    }

    const noise = ctx.createBufferSource()
    noise.buffer = buffer

    const noiseFilter = ctx.createBiquadFilter()
    noiseFilter.type = 'bandpass'
    noiseFilter.frequency.setValueAtTime(noiseFreq, ctx.currentTime)

    const noiseGain = ctx.createGain()
    noiseGain.gain.setValueAtTime(0.09, ctx.currentTime)
    noiseGain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + noiseDecay)

    noise.connect(noiseFilter)
    noiseFilter.connect(noiseGain)
    noiseGain.connect(ctx.destination)

    noise.start(ctx.currentTime)
    noise.stop(ctx.currentTime + noiseDecay)

    const blipDecay = 0.03
    const oscillator = ctx.createOscillator()
    const oscGain = ctx.createGain()

    oscillator.type = 'square'
    oscillator.frequency.setValueAtTime(blipFreq, ctx.currentTime)

    oscGain.gain.setValueAtTime(0.035, ctx.currentTime)
    oscGain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + blipDecay)

    oscillator.connect(oscGain)
    oscGain.connect(ctx.destination)

    oscillator.start(ctx.currentTime)
    oscillator.stop(ctx.currentTime + blipDecay)
}

export function playKeystrokeSound() {
    clickSound(2600, 1400)
}

export function playBackspaceSound() {
    clickSound(1400, 700)
}