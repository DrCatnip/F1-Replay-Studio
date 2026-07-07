from PyQt6.QtWidgets import (
    QMainWindow
)

from app.constants import *

from ui.workspace import Workspace


class MainWindow(QMainWindow):

    def __init__(self):

        super().__init__()

        self.setWindowTitle(
            APP_NAME
        )

        self.resize(
            WINDOW_WIDTH,
            WINDOW_HEIGHT
        )

        self.workspace = Workspace()

        self.setCentralWidget(
            self.workspace
        )