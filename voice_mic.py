#!/usr/bin/env python3
"""Voice Agent - Production Ready Version"""
import os

# Set API key
os.environ['MISTRAL_API_KEY'] = 'xcduBttqCtCwjHyEJoo5iVyp1kEGsRRg'

# Configuration flags
DEBUG = os.getenv('DEBUG', 'False').lower() in ('1', 'true', 'yes')

# Header printing moved into main guard to avoid side effects on import

import sounddevice as sd
import soundfile as sf
import numpy as np
from mistralai import Mistral
import speech_recognition as sr
import time
import re
import string

# debug helper: list available audio devices when DEBUG is enabled
if DEBUG:
    try:
        print("[debug] sounddevice default device:", sd.default.device)
        print("[debug] available devices:")
        for idx, dev in enumerate(sd.query_devices()):
            print(f"[debug] {idx}: {dev['name']} (in:{dev['max_input_channels']}, out:{dev['max_output_channels']})")
    except Exception as e:
        print(f"[debug] could not query devices: {e}")

print("✅ All modules loaded\n")

client = Mistral(api_key='xcduBttqCtCwjHyEJoo5iVyp1kEGsRRg')
SAMPLE_RATE = 16000

def clean_text_for_speech(text):
    """Remove emojis and punctuation marks for cleaner speech output"""
    # Remove emojis (Unicode ranges for emojis)
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"  # emoticons
        "\U0001F300-\U0001F5FF"  # symbols & pictographs
        "\U0001F680-\U0001F6FF"  # transport & map symbols
        "\U0001F1E0-\U0001F1FF"  # flags (iOS)
        "\U00002700-\U000027BF"  # dingbats
        "\U0001f926-\U0001f937"  # gestures
        "\U00010000-\U0010ffff"  # other unicode
        "\u2640-\u2642"  # gender symbols
        "\u2600-\u2B55"  # misc symbols
        "\u200d"  # zero width joiner
        "\u23cf"  # eject symbol
        "\u23e9"  # fast forward
        "\u231a"  # watch
        "\ufe0f"  # variation selector
        "\u3030"  # wavy dash
        "]+",
        flags=re.UNICODE
    )
    text = emoji_pattern.sub('', text)
    
    # Remove punctuation marks
    text = text.translate(str.maketrans('', '', string.punctuation))
    
    # Clean up extra whitespace
    text = ' '.join(text.split())
    
    return text

def record_audio():
    """Record audio with smart silence detection"""
    # allow long conversation window (3‑4 minutes) or override via env
    DURATION = int(os.getenv('MAX_RECORD_SEC', '240'))  # seconds
    if DEBUG:
        # shorter duration for debugging
        DURATION = 10
    
    print(f"🎤 Recording (max {DURATION} seconds) - speak anytime, silence will be monitored\n")
    print("   (press Ctrl-C to cancel)")
    
    chunk_duration = 0.5
    chunk_samples = int(chunk_duration * SAMPLE_RATE)
    chunks_count = int(DURATION / chunk_duration)
    
    # RMS threshold for silence. Lower if your mic is noisy.
    silence_threshold = 0.005  # adjusted to catch quieter background noise periods
    silence_limit = int(5 / chunk_duration)  # 5 seconds of silence
    silence_count = 0
    prompted = False
    audio_chunks = []
    
    try:
        # choose default input device if none specified
        try:
            chosen_device = sd.default.device[0]  # input device index
        except Exception:
            chosen_device = None
        if DEBUG:
            print(f"[debug] using input device: {chosen_device}")
        with sd.InputStream(device=chosen_device, samplerate=SAMPLE_RATE, channels=1, 
                          dtype='float32', blocksize=chunk_samples) as stream:
            for i in range(chunks_count):
                if DEBUG and i % int(1/chunk_duration) == 0:
                    # print status every second
                    print(f"[debug] recording chunk {i}/{chunks_count}")
                chunk, _ = stream.read(chunk_samples)
                
                if chunk is not None:
                    audio_chunks.append(chunk.flatten())
                    
                    rms = np.sqrt(np.mean(chunk**2))
                    
                    # debug output for each chunk
                    if DEBUG:
                        print(f"[debug] chunk={i} rms={rms:.6f} silence_count={silence_count} prompted={prompted}")
                    # RMS display removed for cleaner output
                    
                    # always track silence (regardless of prior speech)
                    if rms > silence_threshold:
                        silence_count = 0
                        if prompted:
                            # user responded after prompt
                            prompted = False
                    else:
                        silence_count += 1
                    
                    # trigger prompt or end on consecutive silence intervals
                    if silence_count >= silence_limit:
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
                            # no response after prompt -> finish recording
                            break
    except Exception as e:
        print(f"❌ Recording error: {e}\n")
    
    print("✅ Recording complete\n")
    return np.concatenate(audio_chunks) if audio_chunks else np.array([])

def is_conversation_end(text):
    """Determine if user text indicates ending the conversation."""
    if not text:
        return False
    lowered = text.lower()
    endings = [
        "that's all", "that is all", "thanks", "thank you",
        "bye", "goodbye", "see you", "see ya", "i'm done", "im done"
    ]
    for phrase in endings:
        if phrase in lowered:
            return True
    return False


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
        
        # Check for user ending the conversation
        if is_conversation_end(text):
            print("\n👋 It sounds like you're finished. Ending session now.\n")
            exit(0)
        
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
                # Clean text for speech (remove emojis and punctuation)
                clean_answer = clean_text_for_speech(answer)
                engine.say(clean_answer)
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

if __name__ == "__main__":
    # Print startup header
    print("\n" + "="*80)
    print("🎤 VOICE AGENT - MICROPHONE INPUT")
    print("="*80 + "\n")
    
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
                # Check for explicit end phrases
                if is_conversation_end(text):
                    print("\n👋 It sounds like you're finished. Ending session now.\n")
                    break
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
                            # Clean text for speech (remove emojis and punctuation)
                            clean_answer = clean_text_for_speech(answer)
                            engine.say(clean_answer)
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
