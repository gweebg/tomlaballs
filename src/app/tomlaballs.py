from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5 import uic


class TomlaballsGUI(QMainWindow):

    def __init__(self):
        super(TomlaballsGUI, self).__init__()
        uic.loadUi("window.ui")
        self.show()


def main():
    app = QApplication([])
    window = TomlaballsGUI()
    app.exec()


if __name__ == '__main__':
    SystemExit(main())



