import httpx
from typing import List, Dict
from app.config import settings

class OllamaClient:
    def __init__(self):
        self.base_url = settings.ollama_url
        self.model = settings.model_name
        self.timeout = 120.0  # Увеличенный таймаут для ответов LLM

    async def generate_response(self, messages: List[Dict[str, str]]) -> str:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                response = await client.post(
                    f"{self.base_url}/api/chat",
                    json={
                        "model": self.model,
                        "messages": messages,
                        "stream": False
                    }
                )
                response.raise_for_status()
                data = response.json()
                return data.get("message", {}).get("content", "Не удалось сгенерировать ответ.")
            except httpx.HTTPError as e:
                return f"Произошла ошибка при обращении к LLM: {str(e)}"
