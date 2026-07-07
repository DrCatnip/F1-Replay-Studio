from PyQt6.QtWidgets import QPushButton


class PrimaryButton(QPushButton):

    def __init__(

        self,

        text

    ):

        super().__init__(text)

        self.setObjectName(
            "PrimaryButton"
        )