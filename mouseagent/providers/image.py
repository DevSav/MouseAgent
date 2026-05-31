from __future__ import annotations

import base64
from io import BytesIO

from mouseagent.screen import Screenshot


def screenshot_to_jpeg_base64(screenshot: Screenshot, quality: int = 82) -> str:
    buffer = BytesIO()
    screenshot.image.save(buffer, format="JPEG", quality=quality)
    return base64.b64encode(buffer.getvalue()).decode("ascii")
