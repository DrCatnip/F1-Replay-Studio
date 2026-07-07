from __future__ import annotations

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QComboBox, QVBoxLayout, QWidget

from ui.widgets.common.panel import Panel
from ui.widgets.common.panel_header import PanelHeader


class DriverPanel(QWidget):
    """Driver selector for replay focus and telemetry sampling."""

    driver_changed = pyqtSignal(str)

    def __init__(self) -> None:
        super().__init__()

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)

        self.panel = Panel()
        self.panel.addWidget(PanelHeader("Driver"))

        self.driver_box = QComboBox()
        self.driver_box.currentTextChanged.connect(self._driver_changed)

        self.panel.addWidget(self.driver_box)
        root.addWidget(self.panel)

    def set_drivers(
        self,
        drivers: list[str]
    ) -> None:
        self.driver_box.blockSignals(True)
        self.driver_box.clear()
        self.driver_box.addItems(drivers)
        self.driver_box.blockSignals(False)

        if drivers:
            self.driver_changed.emit(drivers[0])

    def current_driver(self) -> str:
        return self.driver_box.currentText()

    def _driver_changed(
        self,
        driver: str
    ) -> None:
        if driver:
            self.driver_changed.emit(driver)
