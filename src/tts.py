"""Text-to-Speech module using Piper"""
import subprocess
import numpy as np
import soundfile as sf
from pathlib import Path
from typing import Optional
from config.settings import PIPER_VOICE, SAMPLE_RATE


class PiperTTS:
    """Handles Text-to-Speech using Piper"""
    
    def __init__(self, voice: str = PIPER_VOICE):
        self.voice = voice
        self.sample_rate = SAMPLE_RATE
        print(f"🎙️  Initializing Piper TTS with voice: {voice}")
        # Note: Piper will be downloaded on first use
        
    def synthesize(self, text: str) -> np.ndarray:
        """
        Convert text to speech
        
        Args:
            text: Text to synthesize
            
        Returns:
            numpy array of audio samples
        """
        print(f"🎵 Synthesizing: '{text[:50]}...'")
        
        if not text or len(text) < 1:
            print("⚠️  No text to synthesize")
            return np.array([])
        
        try:
            # Use piper-tts command line
            # Format: echo "text" | piper --model voice --output audio.wav
            process = subprocess.Popen(
                ['piper', '--model', self.voice, '--output_file', '/tmp/output.wav'],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            stdout, stderr = process.communicate(input=text)
            
            if process.returncode != 0:
                print(f"⚠️  Piper error: {stderr}")
                return np.array([])
            
            # Read the generated audio
            if Path('/tmp/output.wav').exists():
                audio_data, sr = sf.read('/tmp/output.wav', dtype='float32')
                print(f"✅ Synthesis complete ({len(audio_data)} samples)")
                return audio_data
            
        except Exception as e:
            print(f"❌ Synthesis failed: {e}")
            return np.array([])
        
        return np.array([])
    
    def set_voice(self, voice: str) -> None:
        """Change voice model"""
        self.voice = voice
        print(f"🎙️  Voice changed to: {voice}")
