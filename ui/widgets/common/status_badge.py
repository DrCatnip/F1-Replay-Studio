from PyQt6.QtWidgets import QLabel


class StatusBadge(QLabel):
    """Small badge for compact status metadata."""

    def __init__(
        self,
        text: str
    ) -> None:

        super().__init__(
            text
        )

        self.setObjectName(
            "StatusBadge"
        )

    def set_status(
        self,
        text: str
    ) -> None:

        self.setText(
            text
        )
