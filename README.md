# Voice Agent - Free AI-Powered Voice Assistant

A complete voice agent built with **100% free, open-source components** and **Mistral's free API tier**.

```
🎤 Whisper (STT)  → Your Voice
         ↓
🤖 Mistral LLM    → Intelligence  
         ↓
🔊 Piper TTS      → Voice Response
```

## ✨ Features

- **Speech-to-Text**: OpenAI Whisper (tiny/base models, CPU)
- **LLM Intelligence**: Mistral Small 24B (free tier: $0.05/$0.08 per 1M tokens)
- **Text-to-Speech**: Piper TTS (open-source, CPU)
- **Agent Orchestration**: LangGraph for workflow management
- **Audio I/O**: PyAudio for microphone/speaker integration
- **100% Local Processing**: No cloud dependencies except LLM

## 💰 Cost Estimate

For a PoC with 1000 demo interactions:
- **Local Components**: FREE ✅
- **Mistral API**: ~$0.01 total (~1000 words × free tier pricing)
- **Total**: < $0.01 🎉

## 🚀 Quick Start

### 1. Clone and Install

```bash
cd "Voice Agent"
python setup.py
pip install -r requirements.txt
```

### 2. Get Mistral API Key

1. Visit https://console.mistral.ai/
2. Sign up (free account)
3. Generate API key
4. Copy to `.env` file:

```env
MISTRAL_API_KEY=your_key_here
```

### 3. Download Models (First Time)

```bash
# Whisper STT model (~140MB for 'base')
python -c "import whisper; whisper.load_model('base')"

# Or for faster inference (but less accurate):
# python -c "import whisper; whisper.load_model('tiny')"
```

### 4. Run the Agent

```bash
python -m src.voice_agent
```

#### Text Mode (Recommended for Testing)
```python
from src.voice_agent import VoiceAgent

agent = VoiceAgent()
agent.run_text_interaction("What is machine learning?")
```

#### Voice Mode (Requires Audio Hardware)
```python
agent.run_voice_interaction(duration=5)  # 5-second recording
```

## 📁 Project Structure

```
Voice Agent/
├── src/
│   ├── voice_agent.py      # Main orchestrator
│   ├── agent.py            # LangGraph workflow
│   ├── stt.py              # Whisper STT module
│   ├── llm.py              # Mistral LLM integration
│   ├── tts.py              # Piper TTS module
│   ├── audio_io.py         # PyAudio recording/playback
│   └── __init__.py
├── config/
│   ├── settings.py         # Configuration
│   └── __init__.py
├── models/                 # Cached models directory
├── requirements.txt        # Dependencies
├── setup.py               # Installation script
├── .env.example           # Environment template
└── README.md              # This file
```

## 🔧 Configuration

Edit `config/settings.py`:

```python
# Whisper model: 'tiny' (fastest), 'base', 'small', 'medium', 'large'
WHISPER_MODEL = "base"

# Piper voice options available at https://github.com/rhasspy/piper
PIPER_VOICE = "en_US-lessac-medium"

# Audio settings
SAMPLE_RATE = 16000
```

## 📚 Module Overview

### Audio I/O (`audio_io.py`)
```python
recorder = AudioRecorder()
audio = recorder.record_audio(duration=5)

player = AudioPlayer()
player.play_audio(audio)
```

### Speech-to-Text (`stt.py`)
```python
stt = WhisperSTT(model="base")
text = stt.transcribe(audio_data)
# or: text = stt.transcribe_from_file("audio.wav")
```

### LLM (`llm.py`)
```python
llm = MistralLLM()
response = llm.generate_response(
    prompt="What is AI?",
    system_prompt="You are a helpful assistant...",
    max_tokens=512
)
```

### Text-to-Speech (`tts.py`)
```python
tts = PiperTTS()
audio = tts.synthesize("Hello, how are you?")
```

### Agent Orchestration (`agent.py`)
```python
from src.agent import VoiceAgentGraph

agent = VoiceAgentGraph()
result = agent.run(audio_input)
# result contains: transcription, llm_response, audio_output
```

## 🔄 Complete Workflow Example

```python
from src.voice_agent import VoiceAgent

# Initialize agent
agent = VoiceAgent()

# Method 1: Text input (fastest, no audio hardware needed)
result = agent.run_text_interaction("Tell me a joke")
# Returns: {"user_input": "...", "agent_response": "...", "audio_output": np.array}

# Method 2: Voice input (requires microphone)
result = agent.run_voice_interaction(duration=5)
```

## Advanced Usage

### Custom System Prompts
```python
from config.settings import AGENT_SYSTEM_PROMPT

custom_prompt = """You are a Python programming expert.
Provide concise, accurate code-related answers only."""

response = llm.generate_response(
    prompt="How do I read a file?",
    system_prompt=custom_prompt
)
```

### Streaming Responses
```python
for chunk in llm.generate_response_stream("Your question here"):
    print(chunk, end="", flush=True)
```

### Change Whisper Model
```python
stt = WhisperSTT(model="tiny")  # Faster, less accurate
stt = WhisperSTT(model="base")  # Balanced
stt = WhisperSTT(model="small") # More accurate
```

## ⚠️ Troubleshooting

### PyAudio Installation Issues (Windows)

```bash
pip install pipwin
pipwin install pyaudio
```

### Mistral API Errors

- Check API key in `.env`
- Ensure you have free tier credits (check console.mistral.ai)
- Rate limits: Free tier has generous limits for PoC use

### Whisper Model Download Slow

- First run downloads ~140MB for 'base' model
- Use 'tiny' (~39MB) for faster setup
- Models cached in `~/.cache/whisper/`

### No Audio Devices Found

- Check microphone/speaker connections
- List devices: `python -c "import pyaudio; p = pyaudio.PyAudio(); print([p.get_device_info_by_index(i)['name'] for i in range(p.get_device_count())])"`

## 🎯 Performance Tips

| Action | Optimization |
|--------|--------------|
| **Faster STT** | Use `whisper.load_model('tiny')` |
| **Faster LLM** | Reduce `max_tokens` or use streaming |
| **Lower Latency** | Process text directly, skip STT |
| **Save Bandwidth** | Cache responses or increase context length |

## 📊 Cost Breakdown (1000 demos)

| Component | Cost | Notes |
|-----------|------|-------|
| Whisper | FREE | CPU-based, open-source |
| Piper | FREE | CPU-based, open-source |
| PyAudio | FREE | Standard library |
| LangGraph | FREE | Open-source |
| Mistral API | ~$0.01 | Free tier: $0.05/$0.08 per 1M tokens |
| **Total** | **<$0.01** | Easily scalable to production ✨ |

## 🔐 Privacy & Security

- All audio processing (Whisper, Piper) runs locally
- Only text queries sent to Mistral API
- No personal data stored
- API key protected in `.env` (add to `.gitignore`)

## 📝 Next Steps

1. ✅ Set up and run the basic agent
2. 🎙️ Test with voice input/output
3. 🔧 Customize system prompts for your use case
4. 🚀 Deploy with FastAPI or Flask endpoint
5. 📈 Monitor costs and optimize model selection

## 🤝 Contributing

Feel free to extend this with:
- Custom voice models
- Additional LLM providers
- Web UI with Streamlit
- Docker containerization
- Multi-language support

## 📄 License

This project uses open-source components. See individual projects for licenses:
- Whisper: MIT
- Piper: MIT
- LangGraph: MIT
- Mistral API: Commercial (free tier available)

## 🎉 Resources

- **Mistral API**: https://console.mistral.ai/
- **Whisper**: https://github.com/openai/whisper
- **Piper TTS**: https://github.com/rhasspy/piper
- **LangGraph**: https://langchain-ai.github.io/langgraph/
- **PyAudio**: https://people.csail.mit.edu/hubert/pyaudio/

---

**Happy hacking! 🚀**
