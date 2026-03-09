"""Configuration settings for Voice Agent"""
import os
from dotenv import load_dotenv

load_dotenv()

# Mistral API Configuration
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY", "")
MISTRAL_MODEL = "mistral-small"  # Free tier model (correct name)
MISTRAL_MAX_TOKENS = 512

# Whisper Configuration (Speech-to-Text)
WHISPER_MODEL = "base"  # Options: tiny, base, small, medium, large
WHISPER_DEVICE = "cpu"  # Use "cuda" if GPU available

# Piper Configuration (Text-to-Speech)
PIPER_VOICE = "en_US-lessac-medium"  # Voice model to use
PIPER_DEVICE = "cpu"

# Audio Configuration
SAMPLE_RATE = 16000
CHUNK_SIZE = 1024
CHANNELS = 1
AUDIO_FORMAT = "float32"

# Agent Configuration
AGENT_NAME = "Voice Agent"
AGENT_SYSTEM_PROMPT = """You are a helpful voice assistant powered by Mistral AI. 
You provide concise, clear responses suitable for text-to-speech synthesis.
Keep responses focused and avoid overly complex language.
Aim for responses under 100 words for optimal user experience."""

# Model paths
MODEL_CACHE_DIR = os.path.join(os.path.dirname(__file__), "..", "models")
