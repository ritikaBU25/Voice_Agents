"""Audio I/O module for recording and playing audio using PyAudio"""
import pyaudio
import numpy as np
from typing import Tuple
import soundfile as sf
from config.settings import SAMPLE_RATE, CHUNK_SIZE, CHANNELS, AUDIO_FORMAT


class AudioRecorder:
    """Handles audio recording using PyAudio"""
    
    def __init__(self, sample_rate: int = SAMPLE_RATE, channels: int = CHANNELS):
        self.sample_rate = sample_rate
        self.channels = channels
        self.chunk_size = CHUNK_SIZE
        self.format = pyaudio.paFloat32
        self.audio = pyaudio.PyAudio()
        
    def record_audio(self, duration: int = 5) -> np.ndarray:
        """
        Record audio from microphone for specified duration (in seconds)
        
        Args:
            duration: Recording duration in seconds
            
        Returns:
            numpy array of audio data
        """
        stream = self.audio.open(
            format=self.format,
            channels=self.channels,
            rate=self.sample_rate,
            input=True,
            frames_per_buffer=self.chunk_size
        )
        
        print(f"🎤 Recording for {duration} seconds...")
        frames = []
        
        for _ in range(0, int(self.sample_rate / self.chunk_size * duration)):
            data = stream.read(self.chunk_size)
            frames.append(np.frombuffer(data, dtype=np.float32))
        
        stream.stop_stream()
        stream.close()
        
        audio_data = np.concatenate(frames)
        print("✅ Recording complete")
        return audio_data
    
    def save_audio(self, audio_data: np.ndarray, filepath: str) -> None:
        """Save audio data to file"""
        sf.write(filepath, audio_data, self.sample_rate)
        print(f"💾 Audio saved to {filepath}")
    
    def __del__(self):
        if self.audio:
            self.audio.terminate()


class AudioPlayer:
    """Handles audio playback using PyAudio"""
    
    def __init__(self, sample_rate: int = SAMPLE_RATE):
        self.sample_rate = sample_rate
        self.format = pyaudio.paFloat32
        self.channels = CHANNELS
        self.audio = pyaudio.PyAudio()
        
    def play_audio(self, audio_data: np.ndarray) -> None:
        """
        Play audio data through speakers
        
        Args:
            audio_data: numpy array of audio samples
        """
        stream = self.audio.open(
            format=self.format,
            channels=self.channels,
            rate=self.sample_rate,
            output=True,
            frames_per_buffer=CHUNK_SIZE
        )
        
        print("🔊 Playing audio...")
        stream.write(audio_data.astype(np.float32).tobytes())
        stream.stop_stream()
        stream.close()
        print("✅ Playback complete")
    
    def play_file(self, filepath: str) -> None:
        """Play audio from file"""
        audio_data, sr = sf.read(filepath, dtype='float32')
        if sr != self.sample_rate:
            print(f"⚠️  Warning: File sample rate {sr} != {self.sample_rate}")
        self.play_audio(audio_data)
    
    def __del__(self):
        if self.audio:
            self.audio.terminate()
