from __future__ import annotations

import json
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

from mouseagent.providers.base import AIProvider
from mouseagent.providers.image import screenshot_to_jpeg_base64
from mouseagent.screen import Screenshot


class GeminiProvider(AIProvider):
    def __init__(self, api_key: str, model: str = "gemini-2.5-flash") -> None:
        self.api_key = api_key.strip()
        self.model = model.strip() or "gemini-2.5-flash"

    def ask(self, question: str, screenshot: Screenshot | None = None) -> str:
        if not self.api_key:
            return "Gemini is selected, but no API key is saved. Open Settings and add one."

        parts = [
            {
                "text": (
                    "You are MouseAgent, a concise screen guidance assistant. "
                    "Tell the user what to do next. Do not suggest automatic clicking.\n\n"
                    f"User question: {question}"
                )
            }
        ]

        if screenshot is not None:
            parts.append(
                {
                    "inline_data": {
                        "mime_type": "image/jpeg",
                        "data": screenshot_to_jpeg_base64(screenshot),
                    }
                }
            )

        payload = {
            "contents": [
                {
                    "role": "user",
                    "parts": parts,
                }
            ]
        }

        url = (
            "https://generativelanguage.googleapis.com/v1beta/models/"
            f"{quote(self.model)}:generateContent?key={quote(self.api_key)}"
        )
        request = Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        try:
            with urlopen(request, timeout=45) as response:
                data = json.loads(response.read().decode("utf-8"))
        except HTTPError as error:
            details = error.read().decode("utf-8", errors="replace")
            return f"Gemini request failed ({error.code}).\n\n{details[:600]}"
        except URLError as error:
            return f"Could not reach Gemini.\n\n{error.reason}"
        except TimeoutError:
            return "Gemini request timed out."

        return self._extract_text(data)

    def _extract_text(self, data: dict) -> str:
        try:
            parts = data["candidates"][0]["content"]["parts"]
        except (KeyError, IndexError, TypeError):
            return f"Gemini returned an unexpected response:\n\n{json.dumps(data)[:800]}"

        text = "\n".join(part.get("text", "") for part in parts if part.get("text"))
        return text.strip() or "Gemini returned an empty response."
