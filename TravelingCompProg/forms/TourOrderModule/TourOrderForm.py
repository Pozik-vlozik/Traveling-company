from TourOrderClass import Ui_ToursOrder
from PyQt5.QtWidgets import QMainWindow
from PyQt5 import QtWidgets, QtGui
from TourOrderDBaser import TODBaser, price_list_producing, path_to_db
from PyQt5.QtWidgets import QMessageBox
from docxtpl import DocxTemplate
import openpyxl
from temp import info_note


class TourOrderFormClass(QMainWindow, Ui_ToursOrder):

    def __init__(self, path=path_to_db, parent=None):
        super(TourOrderFormClass, self).__init__()
        self.setupUi(self)
        self.tour_id = -1
        self.tour_name = None
        self.dBaser = TODBaser(path)
        self.parent = parent
        self.msgBox = QMessageBox()
        self.start_date = []
        self.end_date = []
        self.prices = []
        self.valid_tour = True

        self.tourStartDateCb.currentTextChanged.connect(self.start_date_changed)
        self.orderTourBut.clicked.connect(self.order_tour)
        self.backBut.clicked.connect(self.back_to_tours)
        self.printPriceListBut.clicked.connect(self.print_price_list)

    def showEvent(self, a0: QtGui.QShowEvent) -> None:
        self.setup_c_boxes()

    def print_price_list(self):
        try:
            wb = openpyxl.load_workbook("template\\tour_names_templ.xlsx")
            sheet = wb["Лист1"]
            sheet["B1"] = f"{self.tourStartDateCb.currentText()}"
            sheet["B2"] = self.tourEndDateLe.text()
            sheet["B3"] = self.tourPriceLe.text()
            sheet["B5"] = self.dBaser.get_tours_names()
            sheet["B6"] = info_note
            wb.save(f"contracts\\price_list{str(self.tour_id)}.xlsx")
        except Exception:
            self.msg_box("Ошибка!", "Не удалось найти файл шаблона контракта!")

    def order_tour(self):
        if self.valid_tour:
            name = self.nameLe.text()
            surname = self.surnameLe.text()
            patronymic = self.patronymicLe.text()
            phone = self.phoneLe.text()
            order_number = 0
            tours = self.dBaser.get_table_data("tours")
            for tour in tours:
                order_number += int(tour[5])

            if len(name) == 0 or len(surname) == 0 or len(patronymic) == 0 or len(phone) == 0:
                self.msg_box("Внимание!", "Сначала заполните все данные о себе!")
                return

            try:
                doc = DocxTemplate("template\\contract_templ.docx")
                context = {
                            "contract_number": str(order_number),
                            "client_name": f"{name} {surname} {patronymic}",
                            "start_date": self.tourStartDateCb.currentText(),
                            "tour_price": self.tourPriceLe.text(),
                            "tour_name": self.tour_name,
                            "client_phone": phone
                           }
                doc.render(context)
                doc.save(f"contracts\\contract{str(self.tour_id)}.docx")
            except Exception:
                self.msg_box("Ошибка!", "Не удалось найти файл шаблона контракта!")
                return

            try:
                wb = openpyxl.load_workbook("template\\price_list_templ.xlsx")
                sheet = wb["Лист1"]
                sheet["A2"] = f"Дата начала тура - {self.tourStartDateCb.currentText()}"
                sheet["B2"] = f"Дата окончания тура - {self.tourEndDateLe.text()}"
                sheet["C2"] = f"Стоимость тура - {self.tourPriceLe.text()}"
                wb.save(f"contracts\\contract{str(self.tour_id)}.xlsx")
            except Exception:
                self.msg_box("Ошибка!", "Не удалось найти файл шаблона контракта!")
            self.dBaser.inc_orders_amount(self.tour_id)
            self.msg_box("Успех!", "Тур успешна заказан!")
            self.back_to_tours()
        else:
            self.msg_box("Внимание!", "Отсутствуют прайс листы по данному туру!")

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

    def setup_c_boxes(self):
        plists = self.dBaser.get_price_list(self.tour_id)
        if len(plists) == 0:
            self.msg_box("Внимание!", "Отсутствуют прайс листы по данному туру!")
            self.valid_tour = False
            return
        self.start_date, self.end_date, self.prices = price_list_producing(plists)
        self.tourStartDateCb.clear()
        for i in range(len(self.start_date)):
            self.tourStartDateCb.addItem(self.start_date[i])
            self.tourEndDateLe.setText(self.end_date[i])
            self.tourPriceLe.setText(str(self.prices[i]))

    def start_date_changed(self):
        index = self.tourStartDateCb.currentIndex()
        self.tourEndDateLe.setText(self.end_date[index])
        self.tourPriceLe.setText(str(self.prices[index]))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = TourOrderFormClass("../../" + path_to_db)
    MainWindow.show()
    sys.exit(app.exec_())
