# ═══════════════════════════════════════════════════════════════
# OpenClaw - Pickaxe LLM Provider Configuration
# ═══════════════════════════════════════════════════════════════

import os
import logging
from typing import Optional, Dict, Any
import requests

logger = logging.getLogger(__name__)

class PickaxeProvider:
    """
    Pickaxe LLM Provider for OpenClaw
    Main LLM backend with fallback support
    """
    
    def __init__(self):
        self.api_key = os.getenv('PICKAXE_API_KEY', '')
        self.model = os.getenv('PICKAXE_MODEL', 'pickaxe-7b-instruct')
        self.temperature = float(os.getenv('PICKAXE_TEMPERATURE', '0.7'))
        self.max_tokens = int(os.getenv('PICKAXE_MAX_TOKENS', '2048'))
        self.timeout = int(os.getenv('PICKAXE_TIMEOUT', '60'))
        self.base_url = os.getenv('PICKAXE_API_URL', 'https://api.pickaxe.co/v1')
        self.is_configured = bool(self.api_key)
        
        if self.is_configured:
            logger.info(f"✅ Pickaxe provider configured: {self.model}")
        else:
            logger.warning("⚠️  Pickaxe API key not configured - using fallback mode")
    
    def complete(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Generate completion using Pickaxe
        
        Args:
            prompt: User message
            system_prompt: Optional system context
            **kwargs: Additional parameters
            
        Returns:
            Response dict with completion and metadata
        """
        
        if not self.is_configured:
            return self._fallback_response(prompt)
        
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})
            
            payload = {
                "model": self.model,
                "messages": messages,
                "temperature": self.temperature,
                "max_tokens": self.max_tokens,
                "top_p": kwargs.get('top_p', 0.95),
                "frequency_penalty": kwargs.get('frequency_penalty', 0.0),
                "presence_penalty": kwargs.get('presence_penalty', 0.0),
            }
            
            logger.debug(f"🔄 Calling Pickaxe API with model: {self.model}")
            
            response = requests.post(
                f"{self.base_url}/chat/completions",
                json=payload,
                headers=headers,
                timeout=self.timeout
            )
            
            response.raise_for_status()
            data = response.json()
            
            return {
                "status": "success",
                "response": data['choices'][0]['message']['content'],
                "model": self.model,
                "tokens_used": data.get('usage', {}).get('total_tokens', 0),
                "provider": "pickaxe"
            }
            
        except requests.exceptions.Timeout:
            logger.error(f"❌ Pickaxe timeout after {self.timeout}s")
            return self._fallback_response(prompt, reason="timeout")
            
        except requests.exceptions.ConnectionError as e:
            logger.error(f"❌ Pickaxe connection error: {str(e)}")
            return self._fallback_response(prompt, reason="connection_error")
            
        except requests.exceptions.HTTPError as e:
            logger.error(f"❌ Pickaxe HTTP error: {e.response.status_code}")
            return self._fallback_response(prompt, reason="http_error")
            
        except Exception as e:
            logger.error(f"❌ Pickaxe error: {str(e)}")
            return self._fallback_response(prompt, reason="unexpected_error")
    
    def _fallback_response(
        self,
        prompt: str,
        reason: str = "not_configured"
    ) -> Dict[str, Any]:
        """Fallback response when Pickaxe is unavailable"""
        
        return {
            "status": "fallback",
            "response": f"🤖 Fallback mode: {prompt}",
            "model": "local-fallback",
            "provider": "fallback",
            "reason": reason
        }
    
    def stream_complete(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        **kwargs
    ):
        """
        Stream completion from Pickaxe (generator)
        
        Yields: Text chunks as they arrive
        """
        
        if not self.is_configured:
            yield f"[FALLBACK] {prompt}"
            return
        
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})
            
            payload = {
                "model": self.model,
                "messages": messages,
                "temperature": self.temperature,
                "stream": True,
                **kwargs
            }
            
            response = requests.post(
                f"{self.base_url}/chat/completions",
                json=payload,
                headers=headers,
                timeout=self.timeout,
                stream=True
            )
            
            response.raise_for_status()
            
            for line in response.iter_lines():
                if line:
                    data = line.decode('utf-8')
                    if data.startswith('data: '):
                        chunk = data[6:]
                        if chunk != '[DONE]':
                            try:
                                json_data = eval(chunk) if chunk.startswith('{') else {'choices': [{'delta': {'content': chunk}}]}
                                if 'choices' in json_data:
                                    content = json_data['choices'][0].get('delta', {}).get('content', '')
                                    if content:
                                        yield content
                            except:
                                yield chunk
                                
        except Exception as e:
            logger.error(f"Stream error: {str(e)}")
            yield f"[ERROR] {str(e)}"
    
    def count_tokens(self, text: str) -> int:
        """Estimate token count (rough approximation)"""
        return len(text) // 4  # Rough estimate
    
    def health_check(self) -> Dict[str, Any]:
        """Check Pickaxe API health"""
        
        if not self.is_configured:
            return {
                "status": "unconfigured",
                "healthy": False,
                "message": "API key not set"
            }
        
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            # Quick test call
            response = requests.post(
                f"{self.base_url}/chat/completions",
                json={
                    "model": self.model,
                    "messages": [{"role": "user", "content": "ping"}],
                    "max_tokens": 10
                },
                headers=headers,
                timeout=5
            )
            
            if response.status_code == 200:
                return {
                    "status": "healthy",
                    "healthy": True,
                    "model": self.model,
                    "latency_ms": response.elapsed.total_seconds() * 1000
                }
            else:
                return {
                    "status": "error",
                    "healthy": False,
                    "error_code": response.status_code
                }
                
        except Exception as e:
            return {
                "status": "error",
                "healthy": False,
                "error": str(e)
            }

# Global instance
pickaxe = PickaxeProvider()
