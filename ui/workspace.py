from __future__ import annotations

from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6.QtWidgets import QGridLayout, QVBoxLayout, QWidget

from app.settings import ApplicationSettings
from core.replay_controller import ReplayFrame
from core.session_loader import LoadedSession
from ui.panels.control_panel import ControlPanel
from ui.panels.driver_panel import DriverPanel
from ui.panels.leaderboard_panel import LeaderboardPanel
from ui.panels.session_browser import SessionBrowser
from ui.panels.telemetry_panel import TelemetryPanel
from ui.widgets.replay_view import ReplayView
from ui.session_worker import SessionWorker


class Workspace(QWidget):
    """Main application workspace and orchestration boundary."""

    discover_events_requested = pyqtSignal(int)
    discover_sessions_requested = pyqtSignal(int, str)
    load_requested = pyqtSignal(int, str, str)

    def __init__(self) -> None:
        super().__init__()

        self.loaded_session: LoadedSession | None = None
        self.selected_driver = ""
        self._last_telemetry_update = 0
        self._last_leaderboard_update = 0

        self.settings = ApplicationSettings()
        self.worker_thread = QThread(self)
        self.worker = SessionWorker(self.settings.cache_folder)
        self.worker.moveToThread(self.worker_thread)
        self.discover_events_requested.connect(self.worker.discover_events)
        self.discover_sessions_requested.connect(self.worker.discover_sessions)
        self.load_requested.connect(self.worker.load_session)
        self.worker.events_ready.connect(self._events_ready)
        self.worker.sessions_ready.connect(self._sessions_ready)
        self.worker.session_loaded.connect(self._session_loaded)
        self.worker.failed.connect(self._load_failed)
        self.worker_thread.start()

        layout = QGridLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(16)

        self.browser = SessionBrowser()
        self.driver_panel = DriverPanel()
        self.replay = ReplayView()
        self.replay.set_debug_performance(self.settings.debug_performance)
        self.telemetry = TelemetryPanel()
        self.controls = ControlPanel()
        self.leaderboard = LeaderboardPanel()

        left_column = QWidget()
        left_layout = QVBoxLayout(left_column)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(16)
        left_layout.addWidget(self.browser)
        left_layout.addWidget(self.driver_panel)
        left_layout.addWidget(self.leaderboard, 1)

        layout.addWidget(left_column, 0, 0, 2, 1)
        layout.addWidget(self.replay, 0, 1)
        layout.addWidget(self.telemetry, 0, 2)
        layout.addWidget(self.controls, 1, 1, 1, 2)

        layout.setColumnStretch(0, 2)
        layout.setColumnStretch(1, 6)
        layout.setColumnStretch(2, 3)
        layout.setRowStretch(0, 6)
        layout.setRowStretch(1, 1)

        self.browser.session_requested.connect(self.load_session)
        self.browser.year_changed.connect(self.discover_events)
        self.browser.event_changed.connect(self.discover_sessions)
        self.driver_panel.driver_changed.connect(self.set_selected_driver)
        self.controls.play_button.clicked.connect(self.replay.play)
        self.controls.pause_button.clicked.connect(self.replay.pause)
        self.controls.speed_1.clicked.connect(lambda: self.replay.set_speed(1.0))
        self.controls.speed_2.clicked.connect(lambda: self.replay.set_speed(2.0))
        self.controls.speed_4.clicked.connect(lambda: self.replay.set_speed(4.0))
        self.replay.frame_rendered.connect(self.update_frame_dependent_panels)
        self.discover_events(int(self.browser.year_box.currentText()))

    def load_session(
        self,
        year: int,
        event: str,
        session_type: str
    ) -> None:
        self.controls.set_status("Loading session…")
        self.browser.set_loading("Loading session…")
        self.load_requested.emit(year, event, session_type)

    def discover_events(self, year: int) -> None:
        self.controls.set_status("Discovering events…")
        self.discover_events_requested.emit(year)

    def discover_sessions(self, year: int, event: str) -> None:
        self.discover_sessions_requested.emit(year, event)

    def _events_ready(self, _year: int, events: object) -> None:
        self.browser.set_events(events)
        self.controls.set_status("Select a session")

    def _sessions_ready(self, _year: int, _event: str, sessions: object) -> None:
        self.browser.set_sessions(sessions)
        self.browser.set_ready()
        self.controls.set_status("Ready")

    def _load_failed(self, message: str) -> None:
        self.browser.set_ready()
        self.controls.set_status(message)

    def _session_loaded(self, loaded_session: LoadedSession) -> None:

        self.loaded_session = loaded_session
        self.selected_driver = (
            loaded_session.drivers[0]
            if loaded_session.drivers
            else ""
        )

        self.driver_panel.set_drivers(loaded_session.drivers)
        self.leaderboard.update_drivers(
            loaded_session.leaderboard_engine.current_order()
        )
        self.leaderboard.update_rows(loaded_session.leaderboard_rows, self.selected_driver)
        self.replay.load_session(
            reference_track=loaded_session.reference_track,
            drivers=loaded_session.drivers,
            controller=loaded_session.replay_controller,
            year=loaded_session.year,
            event=loaded_session.event,
            session_type=loaded_session.session_type
        )
        self.replay.set_selected_driver(self.selected_driver)
        self.controls.set_status(
            "Session loaded" if loaded_session.drivers
            else "Session metadata loaded — telemetry unavailable"
        )
        self.browser.set_ready()

    def set_selected_driver(
        self,
        driver: str
    ) -> None:
        self.selected_driver = driver
        self.replay.set_selected_driver(driver)
        if self.loaded_session is not None:
            self.leaderboard.update_rows(self.loaded_session.leaderboard_rows, driver)

    def update_frame_dependent_panels(
        self,
        frame: ReplayFrame
    ) -> None:
        if self.loaded_session is None:
            return

        # Telemetry and leaderboard do not need a 30 FPS refresh; render stays
        # smooth while analytical panels update at controlled rates.
        timestamp_ms = int(frame.timestamp.total_seconds() * 1000)
        if timestamp_ms - self._last_telemetry_update < 100:
            return
        self._last_telemetry_update = timestamp_ms
        telemetry = self.loaded_session.telemetry_engine.sample_for_driver_at_time(
            self.selected_driver,
            frame.timestamp
        )
        order = self.loaded_session.leaderboard_engine.current_order()
        position = (
            order.index(self.selected_driver) + 1
            if self.selected_driver in order
            else None
        )

        self.telemetry.update_data(
            self.selected_driver,
            telemetry,
            position
        )

    def shutdown(self) -> None:
        self.worker_thread.quit()
        self.worker_thread.wait(2000)

    def closeEvent(self, event) -> None:
        self.shutdown()
        super().closeEvent(event)
