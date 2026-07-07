from PyQt6.QtWidgets import QPushButton


class SecondaryButton(QPushButton):
    """Secondary command button using the application theme."""

    def __init__(
        self,
        text: str
    ) -> None:

        super().__init__(
            text
        )

        self.setObjectName(
            "SecondaryButton"
        )
