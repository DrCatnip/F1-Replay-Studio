from __future__ import annotations

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QGridLayout, QVBoxLayout, QWidget

from core.replay_controller import ReplayFrame
from core.session_loader import LoadedSession, SessionLoader
from ui.panels.control_panel import ControlPanel
from ui.panels.driver_panel import DriverPanel
from ui.panels.leaderboard_panel import LeaderboardPanel
from ui.panels.session_browser import SessionBrowser
from ui.panels.telemetry_panel import TelemetryPanel
from ui.widgets.replay_view import ReplayView


class Workspace(QWidget):
    """Main application workspace and orchestration boundary."""

    def __init__(self) -> None:
        super().__init__()

        self.loaded_session: LoadedSession | None = None
        self.selected_driver = ""

        layout = QGridLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(16)

        self.browser = SessionBrowser()
        self.driver_panel = DriverPanel()
        self.replay = ReplayView()
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
        self.driver_panel.driver_changed.connect(self.set_selected_driver)
        self.controls.play_button.clicked.connect(self.replay.play)
        self.controls.pause_button.clicked.connect(self.replay.pause)
        self.controls.speed_1.clicked.connect(lambda: self.replay.set_speed(1.0))
        self.controls.speed_2.clicked.connect(lambda: self.replay.set_speed(2.0))
        self.controls.speed_4.clicked.connect(lambda: self.replay.set_speed(4.0))
        self.replay.frame_rendered.connect(self.update_frame_dependent_panels)

    def load_session(
        self,
        year: int,
        event: str,
        session_type: str
    ) -> None:
        self.controls.set_status("Loading session")
        self.setCursor(Qt.CursorShape.WaitCursor)
        QApplication.processEvents()

        try:
            loader = SessionLoader(
                year=year,
                event=event,
                session_type=session_type
            )
            loaded_session = loader.load()
        except Exception as error:
            self.controls.set_status(f"Load failed: {error}")
            return
        finally:
            self.unsetCursor()

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
        self.replay.load_session(
            reference_track=loaded_session.reference_track,
            drivers=loaded_session.drivers,
            controller=loaded_session.replay_controller,
            year=loaded_session.year,
            event=loaded_session.event,
            session_type=loaded_session.session_type
        )
        self.replay.set_selected_driver(self.selected_driver)
        self.controls.set_status("Session loaded")

    def set_selected_driver(
        self,
        driver: str
    ) -> None:
        self.selected_driver = driver
        self.replay.set_selected_driver(driver)

    def update_frame_dependent_panels(
        self,
        frame: ReplayFrame
    ) -> None:
        if self.loaded_session is None:
            return

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
