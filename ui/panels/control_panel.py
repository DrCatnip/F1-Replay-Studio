from __future__ import annotations

from PyQt6.QtWidgets import QHBoxLayout, QWidget

from ui.widgets.common.panel import Panel
from ui.widgets.common.primary_button import PrimaryButton
from ui.widgets.common.secondary_button import SecondaryButton
from ui.widgets.common.status_badge import StatusBadge


class ControlPanel(QWidget):
    """Playback controls for the active replay controller."""

    def __init__(self) -> None:
        super().__init__()

        root = QHBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)

        self.panel = Panel()
        self.panel.layout.setDirection(QHBoxLayout.Direction.LeftToRight)

        self.play_button = PrimaryButton("Play")
        self.pause_button = SecondaryButton("Pause")
        self.speed_1 = SecondaryButton("1x")
        self.speed_2 = SecondaryButton("2x")
        self.speed_4 = SecondaryButton("4x")
        self.status = StatusBadge("No session")

        self.panel.addWidget(self.play_button)
        self.panel.addWidget(self.pause_button)
        self.panel.addWidget(self.speed_1)
        self.panel.addWidget(self.speed_2)
        self.panel.addWidget(self.speed_4)
        self.panel.addStretch()
        self.panel.addWidget(self.status)

        root.addWidget(self.panel)

    def set_status(
        self,
        status: str
    ) -> None:
        self.status.set_status(status)
