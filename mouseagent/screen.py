from __future__ import annotations

import ctypes
import ctypes.wintypes
import os
from dataclasses import dataclass

import mss
from PIL import Image


@dataclass(frozen=True)
class Screenshot:
    image: Image.Image
    width: int
    height: int


@dataclass(frozen=True)
class WindowInfo:
    app_name: str
    window_title: str


class ScreenCapture:
    def get_foreground_hwnd(self) -> int:
        return ctypes.windll.user32.GetForegroundWindow()

    def get_window_info(self, hwnd: int) -> WindowInfo:
        length = ctypes.windll.user32.GetWindowTextLengthW(hwnd)
        buf = ctypes.create_unicode_buffer(length + 1)
        ctypes.windll.user32.GetWindowTextW(hwnd, buf, length + 1)
        title = buf.value

        pid = ctypes.wintypes.DWORD()
        ctypes.windll.user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))

        app_name = "unknown"
        if pid.value:
            PROCESS_QUERY_LIMITED_INFORMATION = 0x1000
            handle = ctypes.windll.kernel32.OpenProcess(
                PROCESS_QUERY_LIMITED_INFORMATION, False, pid.value
            )
            if handle:
                name_buf = ctypes.create_unicode_buffer(260)
                size = ctypes.wintypes.DWORD(260)
                ctypes.windll.kernel32.QueryFullProcessImageNameW(
                    handle, 0, name_buf, ctypes.byref(size)
                )
                ctypes.windll.kernel32.CloseHandle(handle)
                if name_buf.value:
                    app_name = os.path.splitext(os.path.basename(name_buf.value))[0]

        return WindowInfo(app_name=app_name, window_title=title)

    def capture_window(self, hwnd: int) -> Screenshot:
        if not hwnd or ctypes.windll.user32.IsIconic(hwnd):
            return self.capture_primary_screen()

        rect = ctypes.wintypes.RECT()
        ctypes.windll.user32.GetWindowRect(hwnd, ctypes.byref(rect))

        width = rect.right - rect.left
        height = rect.bottom - rect.top

        if width <= 0 or height <= 0:
            return self.capture_primary_screen()

        region = {"top": rect.top, "left": rect.left, "width": width, "height": height}
        with mss.mss() as sc:
            raw = sc.grab(region)
            image = Image.frombytes("RGB", raw.size, raw.rgb)
        return Screenshot(image=image, width=image.width, height=image.height)

    def capture_primary_screen(self) -> Screenshot:
        with mss.mss() as sc:
            monitor = sc.monitors[1]
            raw = sc.grab(monitor)
            image = Image.frombytes("RGB", raw.size, raw.rgb)
            return Screenshot(image=image, width=image.width, height=image.height)
