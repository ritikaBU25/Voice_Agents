# 🎤 Voice Agent - Complete Guide

## ✅ Setup Complete

Your voice agent is now fully configured and ready to use!

### Installation Summary
- ✅ Python 3.14 with virtual environment
- ✅ All dependencies installed (sounddevice, SpeechRecognition, Mistral AI, pyttsx3)
- ✅ Microphone configured (Logi USB Headset - Device #1)
- ✅ Mistral API key configured

---

## 🚀 How to Run

### Step 1: Navigate to the project folder
```powershell
cd "c:\Users\RitikaKulkarni\Documents\Voice Agent\voice_agent"
```

### Step 2: Run the voice agent
```powershell
python voice_mic.py
```

---

## 📋 Usage Guide

When the script starts, you'll see:
```
Options:
1. 🎤 Speak a question
2. ⌨️  Type a question
3. 📋 Show examples
4. 🚪 Exit
```

### Option 1: Speak a Question (Voice Input)
1. Select **1** and press Enter
2. Wait for: `🎤 Recording for 5 seconds... (Speak now!)`
3. **Speak your question clearly**
4. The script will:
   - Record your speech for up to 10 seconds
   - After 5 seconds of silence, ask: `🤔 Are you still there?`
   - If you respond → continue recording
   - If you stay silent → stop recording and process
5. Your speech is converted to text
6. Mistral AI generates a response
7. Choose to hear the response spoken out loud (y/n)

### Option 2: Type a Question
1. Select **2** and press Enter
2. Type your question
3. Get immediate AI response
4. Choose to hear response spoken out loud (y/n)

### Option 3: Show Examples
Shows example questions to ask

### Option 4: Exit
Quit the application

---

## 🔊 Features

✅ **Real-time Speech Detection**
- Automatically detects when you're speaking
- Silence detection after 5 seconds

✅ **"Are you still there?" Prompt**
- After 5 seconds of silence following speech
- Audio prompt with text-to-speech
- Waits another 5 seconds for response

✅ **Speech-to-Text (STT)**
- Google Speech Recognition API
- Converts spoken words to text

✅ **AI Responses**
- Mistral AI (mistral-small model)
- Generates intelligent responses to questions

✅ **Text-to-Speech (TTS)**
- pyttsx3 engine
- Option to listen to AI responses

---

## 🎯 How It Works (Technical)

### Voice Recording Process
```
1. Listens to microphone (Device #1 - Logi USB Headset)
2. Records 0.5-second chunks
3. Calculates RMS for each chunk
4. Compares against threshold (0.003)
   ├─ RMS > 0.003 → Speech detected
   └─ RMS ≤ 0.003 → Silence
5. After 5 seconds of silence + speech → Prompt "Are you still there?"
6. Wait 5 more seconds
7. If no response → Stop recording and process audio
```

### Audio Processing
```
Recording → WAV File → Speech-to-Text → Mistral AI → Response → TTS
```

---

## ⚙️ Configuration

### Audio Device
Currently configured to use: **Logi USB Headset (Device #1)**

To change device:
1. Run: `python diagnose_audio.py`
2. Note the device number you want to use
3. Edit `voice_mic.py`, find: `device=1`
4. Change `1` to your desired device number

### API Key
Configured in `voice_mic.py` and `.env` file
- **File:** `.env`
- **Key:** `MISTRAL_API_KEY=xcduBttqCtCwjHyEJoo5iVyp1kEGsRRg`

### Silence Detection
- **Silence Threshold:** 0.003 RMS
- **Silence Duration to Trigger Prompt:** 5 seconds
- **Duration to Wait After Prompt:** 5 seconds

Edit in `voice_mic.py`:
```python
silence_threshold = 0.003  # RMS threshold
silence_limit = int(5 / chunk_duration)  # Silence duration in seconds
```

---

## 🧪 Testing

### Test Audio Input
```powershell
python test_audio_levels.py
```
Shows real-time audio levels from microphone

### Test with 10-Second Recording
```powershell
python test_mic_10sec.py
```
Records 10 seconds with visual feedback

### Test Complete Flow
```powershell
python test_voice_simple.py
```
Tests recording, transcription, and AI response

---

## 🐛 Troubleshooting

### Issue: Microphone Not Detected
**Solution:**
1. Run: `python diagnose_audio.py`
2. Check if your microphone appears in the list
3. Note the device number
4. Update `device=1` in `voice_mic.py` to your device number

### Issue: Audio Too Quiet
**Solution:**
1. Check Windows volume settings
2. Speak louder and closer to microphone
3. Adjust silence threshold in code (lower value = more sensitive)

### Issue: Speech-to-Text Not Working
**Solution:**
1. Check internet connection (uses Google Speech API)
2. Ensure audio file is valid: `python test_mic_10sec.py`
3. Try with clearer speech

### Issue: Mistral API Error
**Solution:**
1. Verify API key in `.env` file
2. Check internet connection
3. Ensure API key is valid and has credits

---

## 📁 Files

| File | Purpose |
|------|---------|
| `voice_mic.py` | Main voice agent script |
| `voice_agent_final.py` | Alternative version (same functionality) |
| `.env` | API key configuration |
| `requirements.txt` | Python dependencies |
| `diagnose_audio.py` | Diagnose audio devices |
| `test_audio_levels.py` | Test audio input levels |
| `test_mic_10sec.py` | 10-second microphone test |
| `test_voice_simple.py` | Complete flow test |

---

## 🔒 Security Notes

- API key is stored in `.env` file
- Don't share `.env` file publicly
- Keep API key secret

---

## 📞 Support

If you encounter issues:
1. Run diagnostic scripts
2. Check error messages
3. Verify microphone permissions
4. Ensure all dependencies are installed

---

**Happy voice chatting! 🎉**
