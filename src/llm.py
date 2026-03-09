"""Mistral LLM integration module"""
from mistralai import Mistral
from config.settings import MISTRAL_API_KEY, MISTRAL_MODEL, MISTRAL_MAX_TOKENS
from typing import Optional, List


class MistralLLM:
    """Handles LLM interactions with Mistral API"""
    
    def __init__(self, api_key: Optional[str] = None, model: str = MISTRAL_MODEL):
        self.api_key = api_key or MISTRAL_API_KEY
        if not self.api_key:
            raise ValueError("MISTRAL_API_KEY not set in environment or config")
        
        self.model = model
        self.client = Mistral(api_key=self.api_key)
        print(f"🤖 Mistral LLM initialized with model: {model}")
    
    def generate_response(
        self, 
        prompt: str, 
        system_prompt: Optional[str] = None,
        max_tokens: int = MISTRAL_MAX_TOKENS,
        temperature: float = 0.7
    ) -> str:
        """
        Generate response from Mistral LLM
        
        Args:
            prompt: User prompt/question
            system_prompt: System message to guide the model
            max_tokens: Maximum tokens in response
            temperature: Sampling temperature (0-1)
            
        Returns:
            Generated response text
        """
        messages = []
        
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        messages.append({"role": "user", "content": prompt})
        
        print(f"💬 Sending to Mistral: {prompt[:50]}...")
        
        try:
            response = self.client.chat.complete(
                model=self.model,
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature
            )
            
            result = response.choices[0].message.content
            print(f"✅ Response received ({len(result)} chars)")
            return result
            
        except Exception as e:
            print(f"❌ LLM request failed: {e}")
            return "I encountered an error processing your request."
    
    def generate_response_stream(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        max_tokens: int = MISTRAL_MAX_TOKENS
    ):
        """Stream response tokens for real-time processing"""
        messages = []
        
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        messages.append({"role": "user", "content": prompt})
        
        try:
            response = self.client.chat.stream(
                model=self.model,
                messages=messages,
                max_tokens=max_tokens
            )
            
            for chunk in response:
                if hasattr(chunk, 'choices') and len(chunk.choices) > 0:
                    if hasattr(chunk.choices[0], 'delta') and hasattr(chunk.choices[0].delta, 'content'):
                        if chunk.choices[0].delta.content:
                            yield chunk.choices[0].delta.content
                    
        except Exception as e:
            print(f"❌ Streaming failed: {e}")
            yield f"Error: {str(e)}"
