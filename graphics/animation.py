from __future__ import annotations

from PyQt6.QtCore import QObject, QTimer, pyqtSignal


class AnimationController(QObject):
    """Qt timer adapter for the otherwise pure replay engine."""

    tick = pyqtSignal()

    def __init__(
        self,
        interval_milliseconds: int = 20
    ) -> None:

        super().__init__()

        self.interval_milliseconds = interval_milliseconds
        self.timer = QTimer()
        self.timer.timeout.connect(
            self.tick.emit
        )

    def start(self) -> None:
        self.timer.start(
            self.interval_milliseconds
        )

    def stop(self) -> None:
        self.timer.stop()
