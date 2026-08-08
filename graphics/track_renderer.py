from __future__ import annotations

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure

from core.replay_controller import ReplayFrame
from graphics.camera import CameraController
from graphics.car_renderer import CarRenderer


class TrackRenderer:
    """Matplotlib renderer hidden behind the graphics engine boundary."""

    def __init__(self) -> None:
        self.figure = Figure()
        self.canvas = FigureCanvasQTAgg(
            self.figure
        )
        self.axis = self.figure.add_subplot(111)
        self.camera = CameraController()
        self.car_renderer = CarRenderer(
            self.axis
        )
        self._base_limits: tuple[tuple[float, float], tuple[float, float]] | None = None

    def widget(self):
        return self.canvas

    def load_scene(
        self,
        reference_track,
        drivers: list[str],
        title: str = "Session Replay"
    ) -> None:

        self.axis.clear()

        if reference_track is not None:
            x = getattr(reference_track, "x", None)
            y = getattr(reference_track, "y", None)
            if x is None:
                x = reference_track["X"]
                y = reference_track["Y"]
            self.axis.plot(
                x,
                y,
                alpha=0.3
            )

        self.axis.set_aspect(
            "equal"
        )

        self.axis.set_title(
            title
        )
        self._base_limits = (self.axis.get_xlim(), self.axis.get_ylim())

        self.car_renderer = CarRenderer(
            self.axis
        )

        for driver in drivers:
            self.car_renderer.add_driver(
                driver
            )

        self.canvas.draw()

    def render_frame(
        self,
        frame: ReplayFrame
    ) -> None:

        for driver_state in frame.drivers:
            if driver_state.driver not in self.car_renderer.cars:
                self.car_renderer.add_driver(driver_state.driver)

            self.car_renderer.draw_driver(
                driver_state.driver,
                driver_state.x,
                driver_state.y,
                driver_state.selected
            )

        selected = next((state for state in frame.drivers if state.selected), None)
        if self.camera.follow_driver and selected is not None:
            self._focus_on(selected.x, selected.y)

        self.canvas.draw_idle()

    def zoom_in(self) -> None:
        self.camera.zoom_in()
        self._apply_zoom()

    def zoom_out(self) -> None:
        self.camera.zoom_out()
        self._apply_zoom()

    def reset_camera(self) -> None:
        self.camera.reset()
        self._apply_zoom()

    def set_follow_driver(
        self,
        enabled: bool
    ) -> None:

        self.camera.set_follow_driver(
            enabled
        )

    def _apply_zoom(self) -> None:
        if self._base_limits is None:
            return
        x_limits, y_limits = self._base_limits
        x_center = sum(x_limits) / 2
        y_center = sum(y_limits) / 2
        self._set_limits(x_center, y_center)
        self.canvas.draw_idle()

    def _focus_on(self, x: float, y: float) -> None:
        # Matplotlib does not provide a camera object; interpolating the axes
        # centre gives this backend a light-weight smooth follow behaviour.
        current_x = self.axis.get_xlim()
        current_y = self.axis.get_ylim()
        center_x = (current_x[0] + current_x[1]) / 2 + (x - (current_x[0] + current_x[1]) / 2) * 0.14
        center_y = (current_y[0] + current_y[1]) / 2 + (y - (current_y[0] + current_y[1]) / 2) * 0.14
        self._set_limits(center_x, center_y)

    def _set_limits(self, x_center: float, y_center: float) -> None:
        if self._base_limits is None:
            return
        x_limits, y_limits = self._base_limits
        width = (x_limits[1] - x_limits[0]) / self.camera.zoom_level
        height = (y_limits[1] - y_limits[0]) / self.camera.zoom_level
        self.axis.set_xlim(x_center - width / 2, x_center + width / 2)
        self.axis.set_ylim(y_center - height / 2, y_center + height / 2)
