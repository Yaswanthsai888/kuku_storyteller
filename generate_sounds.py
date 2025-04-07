import numpy as np
import wave
import struct
from pathlib import Path

def generate_sine_wave(frequency, duration, sample_rate=44100, amplitude=0.5):
    """Generate a sine wave with given frequency and duration"""
    t = np.linspace(0, duration, int(sample_rate * duration))
    return amplitude * np.sin(2 * np.pi * frequency * t)

def apply_envelope(signal, attack=0.1, decay=0.1, sustain=0.7, release=0.1):
    """Apply ADSR envelope to a signal"""
    samples = len(signal)
    envelope = np.ones(samples)
    
    attack_samples = int(attack * samples)
    decay_samples = int(decay * samples)
    release_samples = int(release * samples)
    
    # Attack phase
    envelope[:attack_samples] = np.linspace(0, 1, attack_samples)
    # Decay phase
    envelope[attack_samples:attack_samples + decay_samples] = np.linspace(1, sustain, decay_samples)
    # Release phase
    envelope[-release_samples:] = np.linspace(sustain, 0, release_samples)
    
    return signal * envelope

def save_wave_file(filename, samples, sample_rate=44100):
    """Save samples to a WAV file"""
    wav_file = wave.open(filename, 'w')
    wav_file.setnchannels(1)  # Mono
    wav_file.setsampwidth(2)  # 2 bytes per sample
    wav_file.setframerate(sample_rate)
    
    # Convert to 16-bit integers
    samples = (samples * 32767).astype(np.int16)
    wav_file.writeframes(samples.tobytes())
    wav_file.close()

def create_tense_ambient():
    """Create tense ambient sound with low rumble and high pitched whistle"""
    duration = 5.0
    sample_rate = 44100
    
    # Low rumble
    rumble = generate_sine_wave(50, duration, amplitude=0.4)
    rumble += generate_sine_wave(55, duration, amplitude=0.3)
    
    # High whistle
    whistle = generate_sine_wave(2000, duration, amplitude=0.1)
    whistle = apply_envelope(whistle, attack=0.2, decay=0.3, sustain=0.4, release=0.1)
    
    combined = rumble + whistle
    return combined / np.max(np.abs(combined))

def create_peaceful_ambient():
    """Create peaceful ambient sound with gentle harmonics"""
    duration = 5.0
    sample_rate = 44100
    
    # Base frequency and harmonics
    frequencies = [256, 384, 512]
    signal = np.zeros(int(sample_rate * duration))
    
    for freq in frequencies:
        harmonic = generate_sine_wave(freq, duration, amplitude=0.3)
        harmonic = apply_envelope(harmonic, attack=0.3, decay=0.2, sustain=0.6, release=0.2)
        signal += harmonic
    
    return signal / np.max(np.abs(signal))

def create_dramatic_ambient():
    """Create dramatic ambient sound with rising tension"""
    duration = 5.0
    sample_rate = 44100
    
    # Rising frequency sweep
    t = np.linspace(0, duration, int(sample_rate * duration))
    freq = np.linspace(200, 400, len(t))
    sweep = 0.5 * np.sin(2 * np.pi * freq * t)
    
    # Add some percussion hits
    percussion = np.zeros_like(t)
    hit_points = np.array([0.5, 1.5, 2.5, 3.5, 4.5]) * sample_rate
    hit_points = hit_points.astype(int)
    
    for hit in hit_points:
        if hit < len(percussion):
            percussion[hit:hit + 100] = np.random.rand(100) * 0.5
    
    combined = sweep + percussion
    return combined / np.max(np.abs(combined))

def main():
    """Generate all mood ambient sounds"""
    sounds_dir = Path("assets/sounds")
    sounds_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate and save each ambient sound
    mood_generators = {
        "tense": create_tense_ambient,
        "peaceful": create_peaceful_ambient,
        "dramatic": create_dramatic_ambient
    }
    
    for mood, generator in mood_generators.items():
        filename = sounds_dir / f"{mood}_ambient.wav"
        samples = generator()
        save_wave_file(str(filename), samples)
        print(f"Generated {mood} ambient sound")

if __name__ == "__main__":
    main()