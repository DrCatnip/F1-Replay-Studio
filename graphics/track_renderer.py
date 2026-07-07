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

    def widget(self):
        return self.canvas

    def load_scene(
        self,
        reference_track,
        drivers: list[str],
        title: str = "Monaco Session Replay"
    ) -> None:

        self.axis.clear()

        if reference_track is not None:
            self.axis.plot(
                reference_track["X"],
                reference_track["Y"],
                alpha=0.3
            )

        self.axis.set_aspect(
            "equal"
        )

        self.axis.set_title(
            title
        )

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

        self.canvas.draw_idle()

    def zoom_in(self) -> None:
        self.camera.zoom_in()

    def zoom_out(self) -> None:
        self.camera.zoom_out()

    def reset_camera(self) -> None:
        self.camera.reset()

    def set_follow_driver(
        self,
        enabled: bool
    ) -> None:

        self.camera.set_follow_driver(
            enabled
        )
