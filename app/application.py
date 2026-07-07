from PyQt6.QtWidgets import QApplication

from app.theme import load_stylesheet
from app.constants import *


class F1ReplayApplication(QApplication):

    def __init__(

        self,

        argv

    ):

        super().__init__(argv)

        self.setApplicationName(

            APP_NAME

        )

        self.setApplicationVersion(

            APP_VERSION

        )

        self.setStyleSheet(

            load_stylesheet()

        )