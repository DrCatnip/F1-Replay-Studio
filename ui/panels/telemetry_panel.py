from __future__ import annotations

from PyQt6.QtWidgets import QGridLayout, QVBoxLayout, QWidget

from ui.widgets.common.metric_card import MetricCard
from ui.widgets.common.panel import Panel
from ui.widgets.common.panel_header import PanelHeader


class TelemetryPanel(QWidget):
    """Telemetry dashboard rendered from reusable metric cards."""

    def __init__(self) -> None:
        super().__init__()

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)

        self.panel = Panel()
        self.panel.addWidget(PanelHeader("Telemetry"))

        grid_host = QWidget()
        grid = QGridLayout(grid_host)
        grid.setContentsMargins(0, 0, 0, 0)
        grid.setSpacing(10)

        self.driver = MetricCard("Driver", "--")
        self.speed = MetricCard("Speed", "--", "km/h")
        self.rpm = MetricCard("RPM", "--")
        self.gear = MetricCard("Gear", "--")
        self.throttle = MetricCard("Throttle", "--", "%")
        self.brake = MetricCard("Brake", "--")
        self.drs = MetricCard("DRS", "--")
        self.position = MetricCard("Position", "--")
        self.tyre = MetricCard("Tyre", "--")
        self.sector = MetricCard("Sector", "--")
        self.lap_time = MetricCard("Lap Time", "--")

        cards = (
            self.driver,
            self.speed,
            self.rpm,
            self.gear,
            self.throttle,
            self.brake,
            self.drs,
            self.position,
            self.tyre,
            self.sector,
            self.lap_time
        )

        for index, card in enumerate(cards):
            grid.addWidget(card, index // 2, index % 2)

        self.panel.addWidget(grid_host)
        self.panel.addStretch()
        root.addWidget(self.panel)

    def update_data(
        self,
        driver: str,
        telemetry: dict[str, object] | None,
        position: int | None = None
    ) -> None:
        self.driver.setValue(driver or "--")

        if telemetry is None:
            return

        self.speed.setValue(_int_or_dash(telemetry.get("speed")))
        self.rpm.setValue(_int_or_dash(telemetry.get("rpm")))
        self.gear.setValue(telemetry.get("gear", "--"))
        self.throttle.setValue(_int_or_dash(telemetry.get("throttle")))
        self.brake.setValue("ON" if telemetry.get("brake") else "OFF")
        self.drs.setValue(telemetry.get("drs", "--"))
        self.position.setValue(position if position is not None else "--")
        self.tyre.setValue(telemetry.get("tyre", "--"))
        self.sector.setValue(telemetry.get("sector", "--"))
        self.lap_time.setValue(telemetry.get("lap_time", "--"))


def _int_or_dash(value: object) -> str:
    if value is None:
        return "--"

    return str(int(value))
