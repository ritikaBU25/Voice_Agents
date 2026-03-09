"""Main Voice Agent - Complete orchestration"""
import numpy as np
from typing import Optional
from src.agent import VoiceAgentGraph
from src.audio_io import AudioRecorder, AudioPlayer
from config.settings import AGENT_NAME


class VoiceAgent:
    """
    Complete Voice Agent combining:
    - Whisper (STT) for speech recognition
    - Mistral LLM for intelligent responses
    - Piper (TTS) for voice synthesis
    - LangGraph for agent orchestration
    """
    
    def __init__(self):
        print(f"\n{'='*60}")
        print(f"🎤 {AGENT_NAME} - Initialization Started")
        print(f"{'='*60}\n")
        
        self.recorder = AudioRecorder()
        self.player = AudioPlayer()
        self.agent = VoiceAgentGraph()
        
        print(f"\n✅ {AGENT_NAME} Ready!\n")
    
    def run_voice_interaction(self, duration: int = 5) -> dict:
        """
        Run complete voice interaction loop:
        1. Record user speech
        2. Transcribe with Whisper
        3. Generate response with Mistral
        4. Synthesize speech with Piper
        5. Play response
        
        Args:
            duration: Recording duration in seconds
            
        Returns:
            Dictionary with interaction results
        """
        print(f"\n{'='*60}")
        print(f"🎤 Starting Voice Interaction ({duration}s recording)")
        print(f"{'='*60}\n")
        
        # Step 1: Record audio
        audio_input = self.recorder.record_audio(duration=duration)
        
        # Step 2-5: Run agent pipeline
        result = self.agent.run(audio_input)
        
        print(f"\n{'='*60}")
        print(f"📊 Interaction Results")
        print(f"{'='*60}")
        print(f"👤 User: {result['user_input']}")
        print(f"🤖 Agent: {result['llm_response']}")
        print(f"{'='*60}\n")
        
        # Play response
        if result["audio_output"] is not None and len(result["audio_output"]) > 0:
            self.player.play_audio(result["audio_output"])
        else:
            print("⚠️  No audio output generated")
        
        return {
            "user_input": result["user_input"],
            "agent_response": result["llm_response"],
            "audio_output": result["audio_output"]
        }
    
    def run_text_interaction(self, text: str) -> dict:
        """
        Run voice agent with text input (skip STT):
        1. Use provided text as user input
        2. Generate response with Mistral
        3. Synthesize speech with Piper
        4. Play response
        
        Args:
            text: User input text
            
        Returns:
            Dictionary with interaction results
        """
        print(f"\n{'='*60}")
        print(f"📝 Starting Text Interaction")
        print(f"{'='*60}\n")
        
        # Create initial state with text input
        initial_state = {
            "audio_input": None,
            "user_input": text,
            "llm_response": "",
            "audio_output": None,
            "conversation_history": []
        }
        
        # Skip transcription, go directly to LLM
        result = self.agent.node_process_llm(initial_state)
        result = self.agent.node_synthesize(result)
        
        print(f"\n{'='*60}")
        print(f"📊 Results")
        print(f"{'='*60}")
        print(f"👤 You: {result['user_input']}")
        print(f"🤖 Agent: {result['llm_response']}")
        print(f"{'='*60}\n")
        
        # Play response
        if result["audio_output"] is not None and len(result["audio_output"]) > 0:
            self.player.play_audio(result["audio_output"])
        else:
            print("⚠️  No audio output generated")
        
        return {
            "user_input": result["user_input"],
            "agent_response": result["llm_response"],
            "audio_output": result["audio_output"]
        }


def main():
    """Main entry point"""
    import sys
    
    try:
        agent = VoiceAgent()
        
        # Demo: Run text interaction first (faster, no audio hardware needed)
        print("\n📌 Running text-based demo...")
        agent.run_text_interaction("What is artificial intelligence?")
        
        # For voice interaction, uncomment below:
        # agent.run_voice_interaction(duration=5)
        
    except KeyboardInterrupt:
        print("\n\n👋 Agent shutting down...")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
