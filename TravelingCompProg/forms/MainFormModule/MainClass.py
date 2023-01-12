from MainForm import Ui_MainWindow
from PyQt5.QtWidgets import QMainWindow
from PyQt5 import QtWidgets


class MainFormClass(QMainWindow, Ui_MainWindow):

    def __init__(self):
        super(MainFormClass, self).__init__()
        self.setupUi(self)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = MainFormClass()
    MainWindow.show()
    sys.exit(app.exec_())
