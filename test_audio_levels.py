#!/usr/bin/env python3
"""Test audio input levels"""
import sounddevice as sd
import numpy as np
import time

SAMPLE_RATE = 16000

print("\n" + "="*80)
print("🎤 AUDIO LEVEL TEST")
print("="*80 + "\n")

print("🎤 Recording for 5 seconds... Speak normally!\n")

chunk_duration = 0.5  # seconds
chunks_to_read = int(5 / chunk_duration)  # 10 chunks for 5 seconds

try:
    with sd.InputStream(samplerate=SAMPLE_RATE, channels=1, dtype='float32') as stream:
        for i in range(chunks_to_read):
            chunk, overflowed = stream.read(int(chunk_duration * SAMPLE_RATE))
            rms = np.sqrt(np.mean(chunk**2))
            max_val = np.max(np.abs(chunk))
            
            print(f"Chunk {i+1}: RMS={rms:.4f}, Max={max_val:.4f}")
            
except Exception as e:
    print(f"Error: {e}")

print("\n✅ Test complete\n")
