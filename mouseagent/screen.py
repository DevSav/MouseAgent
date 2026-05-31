from dataclasses import dataclass

import mss
from PIL import Image


@dataclass(frozen=True)
class Screenshot:
    image: Image.Image
    width: int
    height: int


class ScreenCapture:
    def capture_primary_screen(self) -> Screenshot:
        with mss.mss() as screen_capture:
            monitor = screen_capture.monitors[1]
            raw = screen_capture.grab(monitor)
            image = Image.frombytes("RGB", raw.size, raw.rgb)
            return Screenshot(image=image, width=image.width, height=image.height)

