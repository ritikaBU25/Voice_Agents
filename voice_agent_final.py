#!/usr/bin/env python3
"""Voice Agent - Production Ready Version"""
import os

# Set API key
os.environ['MISTRAL_API_KEY'] = 'xcduBttqCtCwjHyEJoo5iVyp1kEGsRRg'

print("\n" + "="*80)
print("🎤 VOICE AGENT - MICROPHONE INPUT")
print("="*80 + "\n")

import sounddevice as sd
import soundfile as sf
import numpy as np
from mistralai import Mistral
import speech_recognition as sr
import time

print("✅ All modules loaded\n")

client = Mistral(api_key='xcduBttqCtCwjHyEJoo5iVyp1kEGsRRg')
SAMPLE_RATE = 16000

def record_audio():
    """Record audio with smart silence detection"""
    print("🎤 Recording for 5 seconds... (Speak now!)\n")
    
    DURATION = 10  # Total recording duration
    chunk_duration = 0.5
    chunk_samples = int(chunk_duration * SAMPLE_RATE)
    chunks_count = int(DURATION / chunk_duration)
    
    silence_threshold = 0.003
    silence_limit = int(5 / chunk_duration)  # 5 seconds of silence
    silence_count = 0
    has_speech = False
    prompted = False
    audio_chunks = []
    
    try:
        with sd.InputStream(device=1, samplerate=SAMPLE_RATE, channels=1, 
                          dtype='float32', blocksize=chunk_samples) as stream:
            for i in range(chunks_count):
                chunk, _ = stream.read(chunk_samples)
                
                if chunk is not None:
                    audio_chunks.append(chunk.flatten())
                    
                    rms = np.sqrt(np.mean(chunk**2))
                    
                    # Check for speech
                    if rms > silence_threshold:
                        has_speech = True
                        silence_count = 0
                        if prompted:
                            prompted = False
                    else:
                        if has_speech:
                            silence_count += 1
                    
                    # Handle silence after speech
                    if has_speech and silence_count >= silence_limit:
                        if not prompted:
                            print("\n🤔 Are you still there?\n")
                            try:
                                import pyttsx3
                                engine = pyttsx3.init()
                                engine.say("Are you still there?")
                                engine.runAndWait()
                            except:
                                pass
                            prompted = True
                            silence_count = 0
                        else:
                            # No response after prompt, stop
                            break
    except Exception as e:
        print(f"❌ Recording error: {e}\n")
    
    print("✅ Recording complete\n")
    return np.concatenate(audio_chunks) if audio_chunks else np.array([])

def process_audio(audio):
    """Save, transcribe, and get AI response"""
    if audio is None or len(audio) == 0:
        print("❌ No audio captured\n")
        return
    
    # Save audio
    filename = "temp_voice.wav"
    sf.write(filename, audio, SAMPLE_RATE)
    
    # Transcribe
    print("🔄 Converting speech to text...\n")
    try:
        recognizer = sr.Recognizer()
        with sr.AudioFile(filename) as source:
            audio_data = recognizer.record(source)
        text = recognizer.recognize_google(audio_data)
        print(f"📝 You said: {text}\n")
        
        # Get AI response
        print("🤖 Getting AI response...\n")
        response = client.chat.complete(
            model="mistral-small",
            messages=[{"role": "user", "content": text}],
            max_tokens=300
        )
        answer = response.choices[0].message.content
        print(f"🤖 Response:\n{answer}\n")
        
        # Offer to speak response
        speak = input("Speak response? (y/n): ").lower().strip()
        if speak == 'y':
            print("\n🔊 Speaking response...\n")
            try:
                import pyttsx3
                engine = pyttsx3.init()
                engine.say(answer)
                engine.runAndWait()
            except:
                print("(Text-to-speech not available)\n")
            
    except sr.UnknownValueError:
        print("❌ Could not understand audio\n")
    except sr.RequestError as e:
        print(f"❌ API error: {e}\n")
    except Exception as e:
        print(f"❌ Error: {e}\n")
    finally:
        if os.path.exists(filename):
            os.remove(filename)

# Main loop
print("-"*80)
print("VOICE AGENT - INTERACTIVE MODE")
print("-"*80 + "\n")

while True:
    print("\nOptions:")
    print("1. 🎤 Speak a question")
    print("2. ⌨️  Type a question")
    print("3. 📋 Show examples")
    print("4. 🚪 Exit")
    
    choice = input("\nSelect (1-4): ").strip()
    
    if choice == "1":
        audio = record_audio()
        process_audio(audio)
        
    elif choice == "2":
        text = input("\n📝 Type your question: ").strip()
        if text:
            print("\n🤖 Getting AI response...\n")
            try:
                response = client.chat.complete(
                    model="mistral-small",
                    messages=[{"role": "user", "content": text}],
                    max_tokens=300
                )
                answer = response.choices[0].message.content
                print(f"🤖 Response:\n{answer}\n")
                
                speak = input("Speak response? (y/n): ").lower().strip()
                if speak == 'y':
                    print("\n🔊 Speaking response...\n")
                    try:
                        import pyttsx3
                        engine = pyttsx3.init()
                        engine.say(answer)
                        engine.runAndWait()
                    except:
                        print("(Text-to-speech not available)\n")
            except Exception as e:
                print(f"❌ Error: {e}\n")
    
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
