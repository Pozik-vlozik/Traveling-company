from PriceListsClass import Ui_PriceListsForm
from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5 import QtWidgets, QtGui
from dbaser import DBaser, path_to_db, ErrorClass


class PriceListsFormClass(QMainWindow, Ui_PriceListsForm):

    def __init__(self, path=path_to_db, parent=None):
        super(PriceListsFormClass, self).__init__()
        self.setupUi(self)
        self.parent = parent
        self.tour_id = -1
        self.msgBox = QMessageBox()
        self.dBaser = DBaser(path)
        self.backBut.clicked.connect(self.back_to_tours)
        self.addPriceListBut.clicked.connect(self.new_price_list)

    def msg_box(self, title: str, text: str, icon=None):
        self.msgBox.setText(text)
        self.msgBox.setWindowTitle(title)
        if icon is not None:
            self.msgBox.setIcon(icon)
        self.msgBox.exec()

    def back_to_tours(self):
        if self.parent is not None:
            self.hide()
            self.parent.show()

    def new_price_list(self):
        price = self.tourPriceLe.text()
        if price.isdigit():
            if int(price) < 0:
                self.msg_box("Ошибка!", "Цена должна быть положительным числом!")
                return
        else:
            self.msg_box("Ошибка!", "Цена должна быть числом!")
            return
        start_date = get_date(self.startDate)
        finish_date = get_date(self.endDate)
        try:
            self.dBaser.add_data("price_list", [self.tour_id, start_date, finish_date, price])
        except ErrorClass as e:
            e.show_error_message(self)


def get_date(date_edit: QtWidgets.QDateEdit):
    date = ""
    day = date_edit.date().day()
    month = date_edit.date().month()
    if day < 10:
        date += "0"
    date += str(day) + "-"
    if month < 10:
        date += "0"
    date += str(month) + "-" + str(date_edit.date().year())
    return date


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = PriceListsFormClass("../../" + path_to_db)
    MainWindow.show()
    sys.exit(app.exec_())
