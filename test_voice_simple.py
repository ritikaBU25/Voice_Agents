#!/usr/bin/env python3
"""Standalone voice input test - simplified"""
import os
os.environ['MISTRAL_API_KEY'] = 'xcduBttqCtCwjHyEJoo5iVyp1kEGsRRg'

import sounddevice as sd
import soundfile as sf
import numpy as np
import time
from mistralai import Mistral
import speech_recognition as sr

SAMPLE_RATE = 16000
client = Mistral(api_key='xcduBttqCtCwjHyEJoo5iVyp1kEGsRRg')

print("\n" + "="*80)
print("🎤 VOICE INPUT TEST - SIMPLE VERSION")
print("="*80 + "\n")

def record_audio(max_duration=20):
    """Record audio for up to 20 seconds with silence detection"""
    print("🎤 Recording... (Speak now!)\n")
    print("You have up to 20 seconds. Stay silent for 5 seconds to end recording.\n")
    
    chunk_duration = 0.5
    silence_limit = int(5 / chunk_duration)  # 10 chunks = 5 seconds
    silence_count = 0
    audio_chunks = []
    start_time = time.time()
    has_spoken = False
    prompted = False
    
    try:
        with sd.InputStream(device=1, samplerate=SAMPLE_RATE, channels=1, dtype='float32', 
                          blocksize=int(chunk_duration * SAMPLE_RATE)) as stream:
            while time.time() - start_time < max_duration:
                chunk, _ = stream.read(int(chunk_duration * SAMPLE_RATE))
                
                if chunk is not None and len(chunk) > 0:
                    audio_chunks.append(chunk.flatten())
                    
                    rms = np.sqrt(np.mean(chunk**2))
                    
                    # Show real-time status
                    if rms > 0.003:
                        print(f"  🔊 Speaking: RMS = {rms:.6f}", end='\r')
                        silence_count = 0
                        has_spoken = True
                        if prompted:
                            prompted = False
                            print("\n✓ Speech detected - continuing...     \n")
                    else:
                        if has_spoken:
                            print(f"  🤐 Silence:  RMS = {rms:.6f}", end='\r')
                        silence_count += 1
                    
                    # After speech, if silent for 5 seconds, stop
                    if has_spoken and silence_count >= silence_limit:
                        if not prompted:
                            print("\n🤔 Are you still there?\n")
                            prompted = True
                            silence_count = 0
                        else:
                            print("\n⏹️  Stopping recording.\n")
                            break
                            
    except Exception as e:
        print(f"Error: {e}\n")
    
    return np.concatenate(audio_chunks) if audio_chunks else np.array([])

def save_and_transcribe(audio):
    """Save audio and convert to text"""
    if audio is None or len(audio) == 0:
        print("❌ No audio data\n")
        return None
    
    filename = "temp_voice.wav"
    sf.write(filename, audio, SAMPLE_RATE)
    print(f"✅ Audio saved ({len(audio)} samples)\n")
    
    print("🔄 Converting speech to text...\n")
    try:
        recognizer = sr.Recognizer()
        with sr.AudioFile(filename) as source:
            audio_data = recognizer.record(source)
        text = recognizer.recognize_google(audio_data)
        print(f"📝 You said: {text}\n")
        os.remove(filename)
        return text
    except Exception as e:
        print(f"❌ Error: {e}\n")
        if os.path.exists(filename):
            os.remove(filename)
        return None

def get_response(text):
    """Get AI response"""
    if not text:
        return None
    
    print("🤖 Getting AI response...\n")
    try:
        response = client.chat.complete(
            model="mistral-small",
            messages=[{"role": "user", "content": text}],
            max_tokens=300
        )
        answer = response.choices[0].message.content
        print(f"🤖 Response:\n{answer}\n")
        return answer
    except Exception as e:
        print(f"❌ Error: {e}\n")
        return None

# Test
print("Starting test...\n")
audio = record_audio()
print(f"\n✅ Recording complete ({len(audio)} samples)\n")

if len(audio) > 0:
    text = save_and_transcribe(audio)
    if text:
        response = get_response(text)
else:
    print("No audio was captured\n")

print("="*80 + "\n")
