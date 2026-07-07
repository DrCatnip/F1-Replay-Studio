from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout
)

from PyQt6.QtCore import Qt


class MetricCard(QWidget):

    def __init__(
        self,
        title,
        value="--",
        unit=""
    ):

        super().__init__()

        self.setObjectName("MetricCard")

        layout = QVBoxLayout()

        layout.setContentsMargins(
            10,
            10,
            10,
            10
        )

        layout.setSpacing(4)

        self.title = QLabel(title)

        self.title.setObjectName(
            "MetricTitle"
        )

        self.value = QLabel(value)

        self.value.setObjectName(
            "MetricValue"
        )

        self.unit = QLabel(unit)

        self.unit.setObjectName(
            "MetricUnit"
        )

        self.value.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.unit.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        layout.addWidget(
            self.title
        )

        layout.addWidget(
            self.value
        )

        layout.addWidget(
            self.unit
        )

        self.setLayout(layout)

    def setValue(
        self,
        value
    ):

        self.value.setText(
            str(value)
        )

    def setUnit(
        self,
        unit
    ):

        self.unit.setText(
            unit
        )