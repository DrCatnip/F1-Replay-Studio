from PyQt6.QtWidgets import QFrame


class Divider(QFrame):
    """One-pixel themed divider."""

    def __init__(self) -> None:
        super().__init__()
        self.setObjectName(
            "Divider"
        )
        self.setFixedHeight(
            1
        )
