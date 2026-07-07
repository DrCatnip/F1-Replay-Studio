from PyQt6.QtWidgets import QPushButton


class IconButton(QPushButton):
    """Compact themed button for viewport and toolbar actions."""

    def __init__(
        self,
        text: str,
        tooltip: str = ""
    ) -> None:

        super().__init__(
            text
        )

        self.setObjectName(
            "IconButton"
        )

        if tooltip:
            self.setToolTip(
                tooltip
            )
