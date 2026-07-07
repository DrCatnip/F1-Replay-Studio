from __future__ import annotations


class CameraController:
    """Tracks viewport-level camera preferences for the renderer."""

    def __init__(self) -> None:
        self.zoom_level = 1.0
        self.follow_driver = False

    def zoom_in(self) -> float:
        self.zoom_level = min(
            5.0,
            self.zoom_level + 0.1
        )

        return self.zoom_level

    def zoom_out(self) -> float:
        self.zoom_level = max(
            0.2,
            self.zoom_level - 0.1
        )

        return self.zoom_level

    def reset(self) -> float:
        self.zoom_level = 1.0
        return self.zoom_level

    def set_follow_driver(
        self,
        enabled: bool
    ) -> None:

        self.follow_driver = enabled
