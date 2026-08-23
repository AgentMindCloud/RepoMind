"""LLM client for RepoMind – primary xAI Grok, with simple fallbacks."""
import os
import httpx
from typing import List, Dict, Any, Optional

class LLMClient:
    def __init__(self, api_key: Optional[str] = None, model: str = "grok-3"):
        self.api_key = api_key or os.getenv("XAI_API_KEY")
        self.model = model
        self.base_url = "https://api.x.ai/v1"

    async def chat(self, messages: List[Dict[str, str]], temperature: float = 0.7, max_tokens: int = 4096) -> str:
        if not self.api_key:
            return "[LLM] XAI_API_KEY not set – placeholder response for scaffold."

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens
        }

        async with httpx.AsyncClient(timeout=60.0) as client:
            resp = await client.post(f"{self.base_url}/chat/completions", headers=headers, json=payload)
            resp.raise_for_status()
            data = resp.json()
            return data["choices"][0]["message"]["content"]

    def chat_sync(self, messages: List[Dict[str, str]], temperature: float = 0.7, max_tokens: int = 4096) -> str:
        """Sync wrapper for Actions / simple runners."""
        import asyncio
        return asyncio.run(self.chat(messages, temperature, max_tokens))
