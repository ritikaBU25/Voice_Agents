#!/usr/bin/env python3
"""Direct Voice Input Test - Simple"""
import os
import sys

os.environ['MISTRAL_API_KEY'] = 'xcduBttqCtCwjHyEJoo5iVyp1kEGsRRg'

print("\n" + "="*80)
print("🎤 VOICE AGENT - MICROPHONE INPUT")
print("="*80 + "\n")

# Import modules
import sounddevice as sd
import soundfile as sf
import numpy as np
from mistralai import Mistral
import speech_recognition as sr

print("✅ All modules loaded\n")

# Initialize Mistral
client = Mistral(api_key='xcduBttqCtCwjHyEJoo5iVyp1kEGsRRg')

SAMPLE_RATE = 16000

def record_audio(duration=5):
    """Record audio from microphone"""
    print(f"\n🎤 Recording for {duration} seconds... (Speak now!)\n")
    
    audio = sd.rec(
        int(duration * SAMPLE_RATE),
        samplerate=SAMPLE_RATE,
        channels=1,
        dtype='float32'
    )
    sd.wait()
    
    print("✅ Recording complete\n")
    return audio.flatten()

def save_audio(audio_data, filename="temp_audio.wav"):
    """Save audio as WAV file"""
    sf.write(filename, audio_data, SAMPLE_RATE)
    return filename

def speech_to_text(audio_file):
    """Convert speech to text"""
    print("🔄 Converting speech to text...\n")
    
    recognizer = sr.Recognizer()
    
    with sr.AudioFile(audio_file) as source:
        audio = recognizer.record(source)
    
    try:
        text = recognizer.recognize_google(audio)
        print(f"📝 You said: {text}\n")
        return text
    except sr.UnknownValueError:
        print("❌ Could not understand audio\n")
        return None
    except sr.RequestError as e:
        print(f"❌ API error: {e}\n")
        return None

def get_ai_response(user_text):
    """Get response from Mistral"""
    if not user_text:
        return None
    
    print("🤖 Getting AI response...\n")
    
    response = client.chat.complete(
        model="mistral-small",
        messages=[{"role": "user", "content": user_text}],
        max_tokens=300
    )
    
    answer = response.choices[0].message.content
    print(f"🤖 Response:\n{answer}\n")
    return answer

def speak_response(text):
    """Speak the response"""
    try:
        import pyttsx3
        print("\n🔊 Speaking response...\n")
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
    except:
        pass

# Main loop
print("-"*80)
print("VOICE AGENT - INTERACTIVE MODE")
print("-"*80 + "\n")

while True:
    print("\nOptions:")
    print("1. 🎤 Speak a question (5 seconds)")
    print("2. ⌨️  Type a question")
    print("3. 📋 Show examples")
    print("4. 🚪 Exit")
    
    choice = input("\nSelect (1-4): ").strip()
    
    if choice == "1":
        audio = record_audio(duration=5)
        audio_file = save_audio(audio)
        
        text = speech_to_text(audio_file)
        
        if text:
            response = get_ai_response(text)
            if response:
                speak = input("Speak response? (y/n): ").lower().strip()
                if speak == 'y':
                    speak_response(response)
        
        if os.path.exists(audio_file):
            os.remove(audio_file)
    
    elif choice == "2":
        text = input("\n📝 Type your question: ").strip()
        if text:
            response = get_ai_response(text)
            if response:
                speak = input("Speak response? (y/n): ").lower().strip()
                if speak == 'y':
                    speak_response(response)
    
    elif choice == "3":
        print("""
📋 Example Questions:
  - "What is artificial intelligence?"
  - "Tell me a fun fact about space"
  - "How do I learn Python?"
  - "What is machine learning?"
  - "Who is Elon Musk?"
        """)
    
    elif choice == "4":
        print("\n👋 Goodbye!\n")
        break
    
    else:
        print("❌ Invalid choice\n")
