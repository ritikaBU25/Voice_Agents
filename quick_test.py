#!/usr/bin/env python3
"""Quick audio capture test"""
import sounddevice as sd
import soundfile as sf
import numpy as np
from speech_recognition import Recognizer, AudioFile

SAMPLE_RATE = 16000

print("\n🎤 Quick Audio Test - 3 seconds\n")

# Record audio
print("Recording...")
audio = sd.rec(int(3 * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=1, dtype='float32')
sd.wait()
print("✅ Recording complete")

# Save it
filename = "test_audio.wav"
sf.write(filename, audio, SAMPLE_RATE)
print(f"✅ Saved to {filename}")

# Try to transcribe it
print("\n🔄 Converting to text...")
try:
    recognizer = Recognizer()
    with AudioFile(filename) as source:
        audio_data = recognizer.record(source)
    
    text = recognizer.recognize_google(audio_data)
    print(f"✅ Transcribed: {text}\n")
except Exception as e:
    print(f"❌ Error: {e}\n")

import os
os.remove(filename)
