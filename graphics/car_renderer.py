from __future__ import annotations

from app.constants import DRIVER_COLORS


class CarRenderer:
    """Creates and updates Matplotlib artists for replay cars."""

    def __init__(
        self,
        axis
    ) -> None:

        self.axis = axis
        self.cars = {}
        self.labels = {}

    def add_driver(
        self,
        driver: str
    ) -> None:

        color = DRIVER_COLORS.get(
            driver,
            "black"
        )

        car, = self.axis.plot(
            [],
            [],
            "o",
            color=color,
            markersize=8
        )

        label = self.axis.text(
            0,
            0,
            driver,
            color=color,
            fontsize=8
        )

        self.cars[driver] = car
        self.labels[driver] = label

    def draw_driver(
        self,
        driver: str,
        x: float,
        y: float,
        selected: bool = False
    ) -> None:

        marker_size = 14 if selected else 8
        font_size = 10 if selected else 8

        self.cars[
            driver
        ].set_markersize(
            marker_size
        )

        self.labels[
            driver
        ].set_fontsize(
            font_size
        )

        self.cars[
            driver
        ].set_data(
            [x],
            [y]
        )

        self.labels[
            driver
        ].set_position(
            (
                x + 20,
                y + 20
            )
        )
