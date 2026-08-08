from __future__ import annotations

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QComboBox, QVBoxLayout, QWidget

from app.constants import DEFAULT_YEAR
from models.session_info import EventInfo, SessionInfo
from ui.widgets.common.panel import Panel
from ui.widgets.common.panel_header import PanelHeader
from ui.widgets.common.primary_button import PrimaryButton


class SessionBrowser(QWidget):
    """Session selector that emits load requests without touching FastF1."""

    session_requested = pyqtSignal(int, str, str)
    year_changed = pyqtSignal(int)
    event_changed = pyqtSignal(int, str)

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

        self.year_box.addItems([str(year) for year in range(DEFAULT_YEAR, 2017, -1)])
        self.year_box.setCurrentText(str(DEFAULT_YEAR))
        self.event_box.addItem("Loading events…")
        self.session_box.addItem("Select an event")
        self.load_button.setEnabled(False)

        self.panel.addWidget(self.year_box)
        self.panel.addWidget(self.event_box)
        self.panel.addWidget(self.session_box)
        self.panel.addStretch()
        self.panel.addWidget(self.load_button)

        root.addWidget(self.panel)

        self.load_button.clicked.connect(self._emit_session_requested)
        self.year_box.currentTextChanged.connect(self._year_changed)
        self.event_box.currentTextChanged.connect(self._event_changed)

    def set_events(self, events: list[EventInfo]) -> None:
        self.event_box.blockSignals(True)
        self.event_box.clear()
        for event in events:
            suffix = f" · Round {event.round_number}" if event.round_number else ""
            self.event_box.addItem(f"{event.name}{suffix}", event.name)
        if not events:
            self.event_box.addItem("No events available")
        self.event_box.blockSignals(False)
        if events:
            self._event_changed(self.event_box.currentText())

    def set_sessions(self, sessions: list[SessionInfo]) -> None:
        self.session_box.clear()
        for session in sessions:
            self.session_box.addItem(session.name, session.code)
        if not sessions:
            self.session_box.addItem("Session data unavailable")
        self.load_button.setEnabled(bool(sessions))

    def set_loading(self, text: str) -> None:
        self.load_button.setText(text)
        self.load_button.setEnabled(False)

    def set_ready(self) -> None:
        self.load_button.setText("Load Session")
        self.load_button.setEnabled(self.session_box.count() and self.session_box.currentData() is not None)

    def _year_changed(self, year: str) -> None:
        if year.isdigit():
            self.set_loading("Loading events…")
            self.year_changed.emit(int(year))

    def _event_changed(self, _text: str) -> None:
        event = self.event_box.currentData()
        if isinstance(event, str):
            self.set_loading("Loading sessions…")
            self.event_changed.emit(int(self.year_box.currentText()), event)

    def _emit_session_requested(self) -> None:
        self.session_requested.emit(
            int(self.year_box.currentText()),
            str(self.event_box.currentData()),
            str(self.session_box.currentData())
        )
