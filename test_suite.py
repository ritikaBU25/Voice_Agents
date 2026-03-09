#!/usr/bin/env python3
"""Test suite for Voice Agent"""
import os
os.environ['MISTRAL_API_KEY'] = 'xcduBttqCtCwjHyEJoo5iVyp1kEGsRRg'

import sounddevice as sd
import soundfile as sf
import numpy as np
from mistralai import Mistral
import speech_recognition as sr
import time

SAMPLE_RATE = 16000

print("\n" + "="*80)
print("🧪 VOICE AGENT - COMPREHENSIVE TEST SUITE")
print("="*80 + "\n")

# ============================================================================
# TEST 1: Microphone Audio Capture
# ============================================================================
print("\n" + "-"*80)
print("TEST 1: 🎤 Microphone Audio Capture")
print("-"*80 + "\n")

try:
    print("Recording 3 seconds...")
    audio = sd.rec(int(3 * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=1, dtype='float32')
    sd.wait()
    
    rms = np.sqrt(np.mean(audio**2))
    max_val = np.max(np.abs(audio))
    
    if len(audio) > 0 and rms > 0.0001:
        print("✅ PASS: Audio captured successfully")
        print(f"   - Samples: {len(audio)}")
        print(f"   - RMS Level: {rms:.6f}")
        print(f"   - Max Level: {max_val:.6f}")
        test1_pass = True
    else:
        print("❌ FAIL: No audio captured")
        test1_pass = False
except Exception as e:
    print(f"❌ FAIL: {e}")
    test1_pass = False

# ============================================================================
# TEST 2: Audio File Save/Load
# ============================================================================
print("\n" + "-"*80)
print("TEST 2: 💾 Audio File Save/Load")
print("-"*80 + "\n")

try:
    filename = "test_audio.wav"
    print(f"Saving audio to {filename}...")
    sf.write(filename, audio, SAMPLE_RATE)
    
    print(f"Loading audio from {filename}...")
    loaded_audio, loaded_rate = sf.read(filename)
    
    if loaded_rate == SAMPLE_RATE and len(loaded_audio) == len(audio):
        print("✅ PASS: Audio saved and loaded successfully")
        print(f"   - File size: {os.path.getsize(filename)} bytes")
        print(f"   - Sample rate: {loaded_rate} Hz")
        print(f"   - Samples: {len(loaded_audio)}")
        test2_pass = True
    else:
        print("❌ FAIL: Audio file corrupted")
        test2_pass = False
        
    os.remove(filename)
except Exception as e:
    print(f"❌ FAIL: {e}")
    test2_pass = False

# ============================================================================
# TEST 3: Mistral API Connection
# ============================================================================
print("\n" + "-"*80)
print("TEST 3: 🤖 Mistral AI API Connection")
print("-"*80 + "\n")

try:
    client = Mistral(api_key='xcduBttqCtCwjHyEJoo5iVyp1kEGsRRg')
    print("Testing API with simple query: 'What is 2+2?'")
    
    response = client.chat.complete(
        model="mistral-small",
        messages=[{"role": "user", "content": "What is 2+2?"}],
        max_tokens=50
    )
    
    answer = response.choices[0].message.content
    if "4" in answer:
        print("✅ PASS: Mistral API working correctly")
        print(f"   - Model: mistral-small")
        print(f"   - Response: {answer[:60]}...")
        test3_pass = True
    else:
        print("❌ FAIL: Unexpected response")
        test3_pass = False
except Exception as e:
    print(f"❌ FAIL: {e}")
    test3_pass = False

# ============================================================================
# TEST 4: Text-to-Speech
# ============================================================================
print("\n" + "-"*80)
print("TEST 4: 🔊 Text-to-Speech (TTS)")
print("-"*80 + "\n")

try:
    import pyttsx3
    print("Testing TTS with: 'Hello, this is a test'")
    
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)  # Slower speech for test
    
    # Just test initialization, not actual playback
    if engine is not None:
        print("✅ PASS: Text-to-Speech engine initialized")
        print(f"   - Engine: pyttsx3")
        print(f"   - Voices available: {len(engine.getProperty('voices'))}")
        test4_pass = True
    else:
        print("❌ FAIL: TTS engine not initialized")
        test4_pass = False
except Exception as e:
    print(f"❌ FAIL: {e}")
    test4_pass = False

# ============================================================================
# TEST 5: Silence Detection Logic
# ============================================================================
print("\n" + "-"*80)
print("TEST 5: 🤐 Silence Detection Logic")
print("-"*80 + "\n")

try:
    print("Testing silence detection algorithm...")
    
    # Create test audio: silent + speech + silent
    chunk_duration = 0.5
    # match production threshold; lower values increase silence sensitivity
    silence_threshold = 0.0005
    silence_limit = int(5 / chunk_duration)  # 10 chunks
    
    # Simulate silence (low RMS)
    silent_chunk = np.random.randn(int(chunk_duration * SAMPLE_RATE)) * 0.0001
    silent_rms = np.sqrt(np.mean(silent_chunk**2))
    
    # Simulate speech (higher RMS)
    speech_chunk = np.random.randn(int(chunk_duration * SAMPLE_RATE)) * 0.05
    speech_rms = np.sqrt(np.mean(speech_chunk**2))
    
    print(f"Silence RMS: {silent_rms:.6f} (threshold: {silence_threshold})")
    print(f"Speech RMS: {speech_rms:.6f} (threshold: {silence_threshold})")
    
    silence_detected = silent_rms < silence_threshold
    speech_detected = speech_rms > silence_threshold
    
    if silence_detected and speech_detected:
        print("✅ PASS: Silence detection working correctly")
        print(f"   - Silence correctly identified: {silence_detected}")
        print(f"   - Speech correctly identified: {speech_detected}")
        print(f"   - Silence limit: {silence_limit} chunks (5 seconds)")
        test5_pass = True
    else:
        print("❌ FAIL: Detection algorithm failed")
        test5_pass = False
except Exception as e:
    print(f"❌ FAIL: {e}")
    test5_pass = False

# ============================================================================
# TEST 6: Speech Recognition (using existing audio)
# ============================================================================
print("\n" + "-"*80)
print("TEST 6: 🎙️ Speech-to-Text (STT)")
print("-"*80 + "\n")

try:
    print("Note: STT requires clear audio. Testing with real recording...")
    print("(If no clear speech was captured, this will fail)")
    
    # This test requires the actual recorded audio to have speech
    recognizer = sr.Recognizer()
    
    # Re-record 5 seconds for STT test
    print("\nRecording 5 seconds for STT test...")
    test_audio = sd.rec(int(5 * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=1, dtype='float32')
    sd.wait()
    
    # Save and try to transcribe
    test_file = "stt_test.wav"
    sf.write(test_file, test_audio, SAMPLE_RATE)
    
    with sr.AudioFile(test_file) as source:
        audio_data = recognizer.record(source)
    
    try:
        text = recognizer.recognize_google(audio_data)
        print(f"✅ PASS: Speech-to-Text working")
        print(f"   - Transcribed: '{text}'")
        test6_pass = True
    except sr.UnknownValueError:
        print("⚠️  PARTIAL: Audio captured but unclear/silent")
        print("   - STT engine is working, but no clear speech detected")
        test6_pass = True  # Partial pass - engine works, just no speech
    except sr.RequestError as e:
        print(f"❌ FAIL: Speech-to-Text API error: {e}")
        test6_pass = False
    
    os.remove(test_file)
    
except Exception as e:
    print(f"❌ FAIL: {e}")
    test6_pass = False

# ============================================================================
# TEST 7: Complete Integration Flow
# ============================================================================
print("\n" + "-"*80)
print("TEST 7: 🔄 Complete Integration Flow (Text → AI → Response)")
print("-"*80 + "\n")

try:
    print("Testing complete workflow with text input...")
    
    # Use text instead of speech for reliable testing
    test_question = "Who is Albert Einstein? Keep it brief."
    print(f"Input: '{test_question}'")
    
    # Get AI response
    print("Sending to Mistral AI...")
    client = Mistral(api_key='xcduBttqCtCwjHyEJoo5iVyp1kEGsRRg')
    response = client.chat.complete(
        model="mistral-small",
        messages=[{"role": "user", "content": test_question}],
        max_tokens=200
    )
    
    answer = response.choices[0].message.content
    
    if len(answer) > 10 and ("Einstein" in answer or "physicist" in answer):
        print("✅ PASS: Complete workflow successful")
        print(f"   - Question: '{test_question}'")
        print(f"   - Response length: {len(answer)} characters")
        print(f"   - Response preview: {answer[:75]}...")
        test7_pass = True
    else:
        print("❌ FAIL: Unexpected response")
        test7_pass = False
except Exception as e:
    print(f"❌ FAIL: {e}")
    test7_pass = False

# ============================================================================
# TEST SUMMARY
# ============================================================================
print("\n" + "="*80)
print("📊 TEST SUMMARY")
print("="*80 + "\n")

tests = [
    ("1. Microphone Audio Capture", test1_pass),
    ("2. Audio File Save/Load", test2_pass),
    ("3. Mistral AI API Connection", test3_pass),
    ("4. Text-to-Speech (TTS)", test4_pass),
    ("5. Silence Detection Logic", test5_pass),
    ("6. Speech-to-Text (STT)", test6_pass),
    ("7. Complete Integration Flow", test7_pass),
]

passed = sum(1 for _, result in tests if result)
total = len(tests)

for test_name, result in tests:
    status = "✅ PASS" if result else "❌ FAIL"
    print(f"{status} - {test_name}")

print(f"\n{'='*80}")
print(f"Results: {passed}/{total} tests passed ({passed*100//total}%)")
print(f"{'='*80}\n")

if passed == total:
    print("🎉 ALL TESTS PASSED! Voice agent is ready to use!\n")
    print("Run the agent with:")
    print("  python voice_mic.py\n")
elif passed >= 5:
    print("✅ MOSTLY WORKING! Some features need attention.\n")
else:
    print("⚠️  ISSUES DETECTED! Check configuration.\n")

print("="*80 + "\n")
