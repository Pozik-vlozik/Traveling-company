from control_classes import FormsManager
from PyQt5.QtWidgets import QApplication


def main():
    import sys
    app = QApplication(sys.argv)
    manager = FormsManager()
    manager.start()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
