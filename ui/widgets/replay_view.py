from __future__ import annotations

from typing import Any

import pandas as pd
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QVBoxLayout, QWidget

from core.replay_controller import ReplayController, ReplayFrame
from graphics.animation import AnimationController
from graphics.track_renderer import TrackRenderer
from ui.widgets.timeline import Timeline
from ui.widgets.viewport import Viewport


class ReplayView(QWidget):
    """Qt-facing replay view that delegates replay state and rendering."""

    frame_rendered = pyqtSignal(object)

    def __init__(self) -> None:
        super().__init__()

        self.controller: ReplayController | None = None
        self.renderer = TrackRenderer()
        self.animation = AnimationController(interval_milliseconds=33)
        self.animation.tick.connect(self._on_tick)
        self._follow_enabled = False

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(12)

        self.viewport = Viewport("Session Replay")
        self.viewport.setWidget(self.renderer.widget())

        self.timeline = Timeline()
        self.timeline.scrubbed.connect(self.seek_progress)

        root.addWidget(self.viewport, 1)
        root.addWidget(self.timeline)

        self.viewport.follow_button.clicked.connect(self._toggle_follow)
        self.viewport.reset_button.clicked.connect(self.reset_camera)
        self.viewport.zoom_in_button.clicked.connect(self.zoom_in)
        self.viewport.zoom_out_button.clicked.connect(self.zoom_out)

        self.animation.start()

    def load_session(
        self,
        reference_track: Any,
        drivers: list[str],
        controller: ReplayController,
        year: int,
        event: str,
        session_type: str
    ) -> None:
        self.controller = controller
        self.renderer.load_scene(
            reference_track,
            drivers,
            title=f"{event} {session_type} {year}"
        )
        self.viewport.setSession(event, session_type, year)
        self.viewport.setStatus("Live")
        self._render_current_frame()

    def play(self) -> None:
        if self.controller is not None:
            self.controller.play()
            self.viewport.setStatus("Playing")

    def pause(self) -> None:
        if self.controller is not None:
            self.controller.pause()
            self.viewport.setStatus("Paused")

    def set_speed(
        self,
        speed: float
    ) -> None:
        if self.controller is not None:
            self.controller.set_speed(speed)
            self.viewport.setSpeed(speed)

    def set_selected_driver(
        self,
        driver: str
    ) -> None:
        if self.controller is not None:
            self.controller.set_selected_driver(driver)
            self.viewport.setDriver(driver)

    def seek_progress(
        self,
        progress: float
    ) -> None:
        if self.controller is not None:
            self.controller.seek_progress(progress)
            self._render_current_frame()

    def zoom_in(self) -> None:
        self.renderer.zoom_in()
        self.timeline.set_zoom(self.renderer.camera.zoom_level)

    def zoom_out(self) -> None:
        self.renderer.zoom_out()
        self.timeline.set_zoom(self.renderer.camera.zoom_level)

    def reset_camera(self) -> None:
        self.renderer.reset_camera()
        self.timeline.set_zoom(self.renderer.camera.zoom_level)

    def current_frame(self) -> ReplayFrame | None:
        if self.controller is None:
            return None

        return self.controller.get_current_frame()

    def _toggle_follow(self) -> None:
        self._follow_enabled = not self._follow_enabled
        self.renderer.set_follow_driver(self._follow_enabled)

    def _on_tick(self) -> None:
        if self.controller is None:
            return

        self.controller.advance()
        self._render_current_frame()

    def _render_current_frame(self) -> None:
        frame = self.current_frame()

        if frame is None:
            return

        self.renderer.render_frame(frame)
        self.viewport.setTime(_format_timedelta(frame.timestamp))
        self.viewport.setSpeed(frame.speed)
        self.viewport.setDriver(frame.selected_driver)
        self.timeline.set_progress(frame.progress)
        self.timeline.set_time(
            _format_timedelta(frame.timestamp - frame.start_time),
            _format_timedelta(frame.end_time - frame.start_time)
        )
        self.frame_rendered.emit(frame)


def _format_timedelta(value: pd.Timedelta) -> str:
    total_milliseconds = max(0, int(value.total_seconds() * 1000))
    minutes, remainder = divmod(total_milliseconds, 60000)
    seconds, milliseconds = divmod(remainder, 1000)

    return f"{minutes:02d}:{seconds:02d}.{milliseconds:03d}"
