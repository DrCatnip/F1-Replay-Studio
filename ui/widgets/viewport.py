from __future__ import annotations

from PyQt6.QtWidgets import QFrame, QHBoxLayout, QLabel, QVBoxLayout, QWidget

from ui.widgets.common.icon_button import IconButton
from ui.widgets.common.secondary_button import SecondaryButton
from ui.widgets.common.status_badge import StatusBadge


class Viewport(QWidget):
    """Professional replay viewport container for the active renderer."""

    def __init__(
        self,
        title: str = "Replay View"
    ) -> None:
        super().__init__()

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        header = QFrame()
        header.setObjectName("ViewportHeader")

        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(12, 8, 12, 8)
        header_layout.setSpacing(8)

        self.title_label = QLabel(title)
        self.title_label.setObjectName("ViewportTitle")

        self.driver_badge = StatusBadge("Driver --")

        self.session_label = QLabel("Select a session to begin")
        self.session_label.setObjectName("ViewportSubtitle")

        header_layout.addWidget(self.title_label)
        header_layout.addStretch()
        header_layout.addWidget(self.driver_badge)
        header_layout.addWidget(self.session_label)

        self.content = QFrame()
        self.content_layout = QVBoxLayout(self.content)
        self.content_layout.setContentsMargins(0, 0, 0, 0)

        footer = QFrame()
        footer.setObjectName("ViewportFooter")

        footer_layout = QHBoxLayout(footer)
        footer_layout.setContentsMargins(10, 6, 10, 6)
        footer_layout.setSpacing(8)

        self.follow_button = SecondaryButton("Follow Car")
        self.reset_button = SecondaryButton("Reset Camera")
        self.zoom_in_button = IconButton("+", "Zoom in")
        self.zoom_out_button = IconButton("-", "Zoom out")
        self.fullscreen_button = IconButton("[]", "Fullscreen")

        self.time_label = QLabel("00:00.000")
        self.time_label.setObjectName("ViewportTime")

        self.speed_badge = StatusBadge("1.0x")
        self.fps_badge = StatusBadge("60 FPS")
        self.status_badge = StatusBadge("Ready")

        footer_layout.addWidget(self.follow_button)
        footer_layout.addWidget(self.reset_button)
        footer_layout.addWidget(self.zoom_in_button)
        footer_layout.addWidget(self.zoom_out_button)
        footer_layout.addWidget(self.fullscreen_button)
        footer_layout.addStretch()
        footer_layout.addWidget(self.speed_badge)
        footer_layout.addWidget(self.fps_badge)
        footer_layout.addWidget(self.status_badge)
        footer_layout.addWidget(self.time_label)

        root.addWidget(header)
        root.addWidget(self.content, 1)
        root.addWidget(footer)

    def setWidget(
        self,
        widget: QWidget
    ) -> None:
        self.content_layout.addWidget(widget)

    def setTime(
        self,
        text: str
    ) -> None:
        self.time_label.setText(text)

    def setSession(
        self,
        track: str,
        session: str,
        year: int
    ) -> None:
        self.session_label.setText(f"{track} - {session} - {year}")

    def setDriver(
        self,
        driver: str
    ) -> None:
        self.driver_badge.set_status(f"Driver {driver}")

    def setSpeed(
        self,
        speed: float
    ) -> None:
        self.speed_badge.set_status(f"{speed:.1f}x")

    def setStatus(
        self,
        status: str
    ) -> None:
        self.status_badge.set_status(status)

    def setFps(self, fps: int) -> None:
        self.fps_badge.set_status(f"{fps} FPS")
