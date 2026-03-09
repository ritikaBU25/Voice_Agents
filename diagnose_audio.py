#!/usr/bin/env python3
"""Diagnose audio devices and issues"""
import sounddevice as sd
import numpy as np

print("\n" + "="*80)
print("🔍 AUDIO DEVICE DIAGNOSTIC")
print("="*80 + "\n")

# List all audio devices
print("📋 Available Audio Devices:\n")
devices = sd.query_devices()
print(devices)

# Try to find the default input device
default_input = sd.default.device[0]
print(f"\n✓ Default input device: {default_input}")

# Test recording from default device
print("\n🎤 Testing audio input...")
print("Recording for 3 seconds with default device...\n")

try:
    SAMPLE_RATE = 16000
    DURATION = 3
    
    audio = sd.rec(int(DURATION * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=1, dtype='float32')
    sd.wait()
    
    rms = np.sqrt(np.mean(audio**2))
    max_val = np.max(np.abs(audio))
    
    print(f"✅ Recording successful!")
    print(f"   RMS: {rms:.6f}")
    print(f"   Max: {max_val:.6f}")
    print(f"   Samples: {len(audio)}")
    
    if rms < 0.0001:
        print("\n⚠️  WARNING: Very low audio levels - microphone may not be working")
    elif rms < 0.001:
        print("\n⚠️  WARNING: Low audio levels - check microphone settings")
    else:
        print("\n✅ Audio levels look good!")
    
except Exception as e:
    print(f"❌ Error: {e}")

print("\n" + "="*80)
