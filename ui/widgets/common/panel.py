from PyQt6.QtWidgets import (
    QFrame,
    QVBoxLayout
)


class Panel(QFrame):

    def __init__(self):

        super().__init__()

        self.layout = QVBoxLayout()

        self.layout.setContentsMargins(
            16,
            16,
            16,
            16
        )

        self.layout.setSpacing(
            12
        )

        self.setLayout(
            self.layout
        )

        self.setObjectName(
            "Panel"
        )

    def addWidget(
        self,
        widget
    ):

        self.layout.addWidget(
            widget
        )

    def addStretch(self):

        self.layout.addStretch()