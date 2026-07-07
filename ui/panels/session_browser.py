from __future__ import annotations

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QComboBox, QVBoxLayout, QWidget

from app.constants import DEFAULT_EVENT, DEFAULT_SESSION, DEFAULT_YEAR
from ui.widgets.common.panel import Panel
from ui.widgets.common.panel_header import PanelHeader
from ui.widgets.common.primary_button import PrimaryButton


class SessionBrowser(QWidget):
    """Session selector that emits load requests without touching FastF1."""

    session_requested = pyqtSignal(int, str, str)

    def __init__(self) -> None:
        super().__init__()

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)

        self.panel = Panel()
        self.panel.addWidget(PanelHeader("Session Browser"))

        self.year_box = QComboBox()
        self.event_box = QComboBox()
        self.session_box = QComboBox()
        self.load_button = PrimaryButton("Load Session")

        self.year_box.addItems(["2024", "2023", "2022"])
        self.year_box.setCurrentText(str(DEFAULT_YEAR))

        self.event_box.addItems(["Monaco", DEFAULT_EVENT])
        self.event_box.setCurrentText(DEFAULT_EVENT)

        self.session_box.addItem("Qualifying", "Q")
        self.session_box.addItem("Race", "R")
        self.session_box.addItem("Practice 1", "FP1")
        self.session_box.addItem("Practice 2", "FP2")
        self.session_box.addItem("Practice 3", "FP3")

        for index in range(self.session_box.count()):
            if self.session_box.itemData(index) == DEFAULT_SESSION:
                self.session_box.setCurrentIndex(index)
                break

        self.panel.addWidget(self.year_box)
        self.panel.addWidget(self.event_box)
        self.panel.addWidget(self.session_box)
        self.panel.addStretch()
        self.panel.addWidget(self.load_button)

        root.addWidget(self.panel)

        self.load_button.clicked.connect(self._emit_session_requested)

    def _emit_session_requested(self) -> None:
        self.session_requested.emit(
            int(self.year_box.currentText()),
            self.event_box.currentText(),
            str(self.session_box.currentData())
        )
