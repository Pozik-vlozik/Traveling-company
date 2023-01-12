from PyQt5.QtWidgets import QMessageBox, QWidget


class ErrorClass(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return "ErrorClass, {} ".format(self.message)
        else:
            return "ErrorClass has been rised!"

    def show_error_message(self, form: QWidget, icon=None):
        msg = QMessageBox(form)
        msg.setWindowTitle("Внимание!")
        msg.setText(self.message)
        if icon is None:
            msg.setIcon(QMessageBox.Warning)
        else:
            msg.setIcon(icon)
        msg.exec_()

