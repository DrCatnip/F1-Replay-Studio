from __future__ import annotations

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QSlider, QVBoxLayout, QWidget

from ui.widgets.common.status_badge import StatusBadge


class Timeline(QWidget):
    """Replay timeline with scrubbing and compact playback metadata."""

    scrubbed = pyqtSignal(float)

    def __init__(self) -> None:
        super().__init__()

        self.setObjectName("Timeline")

        root = QVBoxLayout(self)
        root.setContentsMargins(12, 10, 12, 10)
        root.setSpacing(8)

        header = QHBoxLayout()
        header.setContentsMargins(0, 0, 0, 0)
        header.setSpacing(8)

        self.current_label = QLabel("00:00.000")
        self.duration_label = QLabel("00:00.000")
        self.zoom_badge = StatusBadge("1.0x")

        header.addWidget(self.current_label)
        header.addStretch()
        header.addWidget(QLabel("Zoom"))
        header.addWidget(self.zoom_badge)
        header.addWidget(self.duration_label)

        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setRange(0, 1000)
        self.slider.setSingleStep(1)
        self.slider.setPageStep(25)
        self.slider.setTracking(True)
        self.slider.valueChanged.connect(self._emit_scrubbed)

        markers = QHBoxLayout()
        markers.setContentsMargins(0, 0, 0, 0)
        markers.setSpacing(6)

        for label in ("Yellow", "SC", "VSC", "Pit", "Fastest", "Sectors"):
            markers.addWidget(StatusBadge(label))

        markers.addStretch()

        root.addLayout(header)
        root.addWidget(self.slider)
        root.addLayout(markers)

    def set_progress(
        self,
        progress: float
    ) -> None:
        value = int(max(0.0, min(1.0, progress)) * 1000)

        self.slider.blockSignals(True)
        self.slider.setValue(value)
        self.slider.blockSignals(False)

    def set_time(
        self,
        current_text: str,
        duration_text: str
    ) -> None:
        self.current_label.setText(current_text)
        self.duration_label.setText(duration_text)

    def set_zoom(
        self,
        zoom: float
    ) -> None:
        self.zoom_badge.set_status(f"{zoom:.1f}x")

    def _emit_scrubbed(
        self,
        value: int
    ) -> None:
        self.scrubbed.emit(value / 1000)
