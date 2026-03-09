"""Speech-to-Text module using Whisper"""
import whisper
import numpy as np
from config.settings import WHISPER_MODEL, WHISPER_DEVICE, SAMPLE_RATE
from typing import Optional


class WhisperSTT:
    """Handles Speech-to-Text using OpenAI Whisper"""
    
    def __init__(self, model: str = WHISPER_MODEL, device: str = WHISPER_DEVICE):
        self.model_name = model
        self.device = device
        print(f"📥 Loading Whisper model: {model} on {device}...")
        self.model = whisper.load_model(model, device=device)
        print("✅ Whisper model loaded")
    
    def transcribe(self, audio_data: np.ndarray, language: Optional[str] = "en") -> str:
        """
        Transcribe audio to text
        
        Args:
            audio_data: numpy array of audio samples (16kHz mono)
            language: Language code (e.g., 'en', 'es', 'fr')
            
        Returns:
            Transcribed text
        """
        print("🔄 Transcribing audio...")
        
        # Normalize audio to [-1, 1] range if needed
        if np.max(np.abs(audio_data)) <= 1:
            audio_normalized = audio_data
        else:
            audio_normalized = audio_data / np.max(np.abs(audio_data))
        
        result = self.model.transcribe(
            audio_normalized,
            language=language,
            fp16=False  # Use FP32 for CPU
        )
        
        text = result["text"].strip()
        print(f"📝 Transcription: {text}")
        return text
    
    def transcribe_from_file(self, filepath: str, language: Optional[str] = "en") -> str:
        """Transcribe from audio file"""
        print(f"📂 Loading audio from {filepath}...")
        audio = whisper.load_audio(filepath)
        return self.transcribe(audio, language)
