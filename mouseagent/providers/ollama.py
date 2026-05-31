from __future__ import annotations

import json
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from mouseagent.providers.base import AIProvider
from mouseagent.providers.image import screenshot_to_jpeg_base64
from mouseagent.screen import Screenshot


class OllamaProvider(AIProvider):
    def __init__(self, base_url: str, model: str = "llama3.2-vision") -> None:
        self.base_url = base_url.rstrip("/") or "http://localhost:11434"
        self.model = model.strip() or "llama3.2-vision"

    def ask(self, question: str, screenshot: Screenshot | None = None) -> str:
        message = {
            "role": "user",
            "content": (
                "You are MouseAgent, a concise screen guidance assistant. "
                "Tell the user what to do next. Do not suggest automatic clicking.\n\n"
                f"User question: {question}"
            ),
        }

        if screenshot is not None:
            message["images"] = [screenshot_to_jpeg_base64(screenshot)]

        payload = {
            "model": self.model,
            "messages": [message],
            "stream": False,
        }

        request = Request(
            f"{self.base_url}/api/chat",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        try:
            with urlopen(request, timeout=90) as response:
                data = json.loads(response.read().decode("utf-8"))
        except HTTPError as error:
            details = error.read().decode("utf-8", errors="replace")
            return f"Ollama request failed ({error.code}).\n\n{details[:600]}"
        except URLError:
            return (
                "Could not reach Ollama. Make sure Ollama is running and the model is installed.\n\n"
                f"Try: ollama pull {self.model}"
            )
        except TimeoutError:
            return "Ollama request timed out."

        message_data = data.get("message", {})
        text = message_data.get("content", "")
        return text.strip() or f"Ollama returned an unexpected response:\n\n{json.dumps(data)[:800]}"
