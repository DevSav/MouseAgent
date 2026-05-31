from collections.abc import Callable


class HotkeyController:
    def __init__(self, on_activate: Callable[[], None]) -> None:
        self.on_activate = on_activate

    def start(self) -> None:
        # TODO: Add a real global shortcut, likely Ctrl+Space or Alt+Space.
        # For now, the overlay can be tested without keyboard permissions.
        return None

