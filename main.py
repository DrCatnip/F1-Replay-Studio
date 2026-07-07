import sys

from app.application import F1ReplayApplication

from ui.windows.main_window import MainWindow


def main():

    app = F1ReplayApplication(
        sys.argv
    )

    window = MainWindow()

    window.show()

    sys.exit(
        app.exec()
    )


if __name__ == "__main__":

    main()