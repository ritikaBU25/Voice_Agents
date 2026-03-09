#!/usr/bin/env python3
"""Simple 10-second recording test with real-time feedback"""
import sounddevice as sd
import numpy as np
import time

SAMPLE_RATE = 16000
DURATION = 10  # 10 seconds

print("\n" + "="*80)
print("🎤 10-SECOND MICROPHONE TEST")
print("="*80 + "\n")

print("Recording for 10 seconds...")
print("Speak to see real-time audio levels\n")

chunk_duration = 0.5
chunk_samples = int(chunk_duration * SAMPLE_RATE)
chunks_total = int(DURATION / chunk_duration)
audio_chunks = []

try:
    with sd.InputStream(device=1, samplerate=SAMPLE_RATE, channels=1, dtype='float32', blocksize=chunk_samples) as stream:
        for i in range(chunks_total):
            chunk, overflowed = stream.read(chunk_samples)
            audio_chunks.append(chunk.flatten())
            
            rms = np.sqrt(np.mean(chunk**2))
            max_val = np.max(np.abs(chunk))
            
            bar_length = int(rms * 500)  # Visual bar
            bar = "█" * bar_length
            
            elapsed = (i + 1) * chunk_duration
            status = "🔊 SPEAKING " if rms > 0.003 else "🤐 SILENT  "
            print(f"[{elapsed:5.1f}s] {status} | RMS: {rms:.6f} | {bar}")
            
except Exception as e:
    print(f"Error: {e}")

print("\n✅ Recording complete!")

if audio_chunks:
    full_audio = np.concatenate(audio_chunks)
    print(f"✓ Captured {len(full_audio)} samples")
    print(f"✓ Duration: {len(full_audio) / SAMPLE_RATE:.2f} seconds")
    print(f"✓ Max RMS: {np.sqrt(np.mean(full_audio**2)):.6f}")

print("\n" + "="*80)
