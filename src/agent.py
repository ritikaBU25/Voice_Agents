"""LangGraph-based agent orchestration for voice agent"""
from typing import TypedDict, List, Optional
from langgraph.graph import StateGraph, END
from config.settings import AGENT_SYSTEM_PROMPT
from src.stt import WhisperSTT
from src.llm import MistralLLM
from src.tts import PiperTTS
import numpy as np


class AgentState(TypedDict):
    """State object for the voice agent workflow"""
    audio_input: Optional[np.ndarray]
    user_input: str
    llm_response: str
    audio_output: Optional[np.ndarray]
    conversation_history: List[dict]


class VoiceAgentGraph:
    """LangGraph-based orchestration for voice agent workflow"""
    
    def __init__(self):
        self.stt = WhisperSTT()
        self.llm = MistralLLM()
        self.tts = PiperTTS()
        self.graph = self._build_graph()
        
    def _build_graph(self):
        """Build the LangGraph workflow"""
        workflow = StateGraph(AgentState)
        
        # Add nodes
        workflow.add_node("transcribe", self.node_transcribe)
        workflow.add_node("process_llm", self.node_process_llm)
        workflow.add_node("synthesize", self.node_synthesize)
        
        # Add edges
        workflow.add_edge("transcribe", "process_llm")
        workflow.add_edge("process_llm", "synthesize")
        workflow.add_edge("synthesize", END)
        
        # Set entry point
        workflow.set_entry_point("transcribe")
        
        return workflow.compile()
    
    def node_transcribe(self, state: AgentState) -> AgentState:
        """Transcribe audio to text"""
        print("\n[STEP 1/3] Transcribing audio...")
        
        if state.get("audio_input") is not None:
            text = self.stt.transcribe(state["audio_input"])
            state["user_input"] = text
        
        return state
    
    def node_process_llm(self, state: AgentState) -> AgentState:
        """Process user input with LLM"""
        print("\n[STEP 2/3] Processing with Mistral LLM...")
        
        response = self.llm.generate_response(
            prompt=state["user_input"],
            system_prompt=AGENT_SYSTEM_PROMPT
        )
        
        state["llm_response"] = response
        
        # Update conversation history
        if "conversation_history" not in state:
            state["conversation_history"] = []
        
        state["conversation_history"].append({
            "role": "user",
            "content": state["user_input"]
        })
        state["conversation_history"].append({
            "role": "assistant",
            "content": response
        })
        
        return state
    
    def node_synthesize(self, state: AgentState) -> AgentState:
        """Synthesize response to speech"""
        print("\n[STEP 3/3] Synthesizing speech...")
        
        audio = self.tts.synthesize(state["llm_response"])
        state["audio_output"] = audio
        
        return state
    
    def run(self, audio_input: np.ndarray) -> AgentState:
        """
        Run the complete voice agent pipeline
        
        Args:
            audio_input: Audio samples from user
            
        Returns:
            Final agent state with all processing results
        """
        initial_state: AgentState = {
            "audio_input": audio_input,
            "user_input": "",
            "llm_response": "",
            "audio_output": None,
            "conversation_history": []
        }
        
        result = self.graph.invoke(initial_state)
        return result
