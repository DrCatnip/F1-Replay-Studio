from __future__ import annotations

from typing import Any


class Scene:
    """Renderer-agnostic scene data for the current replay session."""

    def __init__(self) -> None:
        self.reference_track: Any | None = None
        self.drivers: list[str] = []

    def load(
        self,
        reference_track: Any,
        drivers: list[str]
    ) -> None:

        self.reference_track = reference_track
        self.drivers = list(drivers)
