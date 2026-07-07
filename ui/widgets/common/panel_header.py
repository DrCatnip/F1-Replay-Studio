from PyQt6.QtWidgets import QLabel


class PanelHeader(QLabel):

    def __init__(self, text):

        super().__init__(text)

        self.setObjectName("PanelHeader")