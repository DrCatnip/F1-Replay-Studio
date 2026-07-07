from PyQt6.QtWidgets import QFrame, QVBoxLayout
from PyQt6.QtCore import Qt


class Card(QFrame):
    """
    Base Card widget used throughout the application.
    """

    def __init__(self, title=None):

        super().__init__()

        self.setObjectName("Card")

        self.layout = QVBoxLayout()

        self.layout.setContentsMargins(
            18,
            18,
            18,
            18
        )

        self.layout.setSpacing(12)

        self.setLayout(self.layout)

    def addWidget(self, widget):

        self.layout.addWidget(widget)

    def addStretch(self):

        self.layout.addStretch()

    def setAlignment(self, alignment):

        self.layout.setAlignment(alignment)