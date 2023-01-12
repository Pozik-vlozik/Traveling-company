from PriceListsModule import PriceListsFormClass
from ChangePointsModule import ChangePointsFormClass, CHPDBaser
from TourOrderModule import TourOrderFormClass, TODBaser, price_list_producing

from ToursFormClass import Ui_ShowTours
from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5 import QtWidgets, QtGui
from dbaser import DBaser, path_to_db, ErrorClass, cols_names_rus
from temp import info_note

import matplotlib.pyplot as plt


class ToursFormClass(QMainWindow, Ui_ShowTours):

    def __init__(self, path=path_to_db):
        super(ToursFormClass, self).__init__()
        self.setupUi(self)
        self.priceListFormClass = PriceListsFormClass(path, self)
        self.changePointsFormClass = ChangePointsFormClass(path, self)
        self.tourOrderFormClass = TourOrderFormClass(path, self)
        self.msgBox = QMessageBox()

        self.dBaser = DBaser(path)
        self.todBaser = TODBaser(path)
        self.chpdBaser = CHPDBaser(path)

        self.priceListsBut.clicked.connect(self.show_price_list)
        self.deleteTourBut.clicked.connect(self.delete_tour)
        self.changePointsBut.clicked.connect(self.show_change_points)
        self.orderTourBut.clicked.connect(self.show_tour_order)
        self.infoBut.clicked.connect(self.show_tour_info)
        self.returnBut.clicked.connect(self.return_to_tours)
        self.showHotelsBut.clicked.connect(self.five_star_hotels)
        self.pointsDiagramBut.clicked.connect(self.points_diagram)

    def showEvent(self, a0: QtGui.QShowEvent) -> None:
        self.on_form_show()

    def on_form_show(self):
        try:
            self.tourInfoTe.setVisible(False)
            self.returnBut.setEnabled(False)
            self.dBaser.update_dicts()
            fill_table(self.toursTable, self.dBaser)
            self.toursTable.setColumnHidden(0, True)
        except ErrorClass as e:
            e.show_error_message(self)

    def msg_box(self, title: str, text: str, icon=None):
        self.msgBox.setText(text)
        self.msgBox.setWindowTitle(title)
        if icon is not None:
            self.msgBox.setIcon(icon)
        self.msgBox.exec()

    def points_diagram(self):
        tours = [tour[0] for tour in self.dBaser.get_all_tours()]
        points_amount = []
        for i in range(len(tours)):
            points_amount.append(len(self.chpdBaser.get_visit_points(tours[i])))
            tours[i] = self.dBaser.get_tour_name(tours[i])
        plt.bar([x for x in range(len(tours))], points_amount)
        for i in range(len(tours)):
            plt.text(i, points_amount[i], tours[i][0][0])
        plt.show()

    def show_change_points(self):
        if len(self.toursTable.selectedItems()) == 1:
            self.changePointsFormClass.tour_id = self.toursTable.item(self.toursTable.currentRow(), 0).text()
            self.hide()
            self.changePointsFormClass.show()

    def show_tour_order(self):
        if len(self.toursTable.selectedItems()) == 1:
            tour_id = int(self.toursTable.item(self.toursTable.currentRow(), 0).text())
            vis_points = self.chpdBaser.get_visit_points(tour_id)
            price_lists = self.todBaser.get_price_list(tour_id)
            if len(vis_points) == 0:
                self.msg_box("Внимание!", "У тура должен быть хотя бы один город для посещения!")
                return
            elif len(price_lists) == 0:
                self.msg_box("Внимание!", "У тура должен быть хотя бы один прайс лист!")
                return
            else:
                self.tourOrderFormClass.tour_id = tour_id
                self.tourOrderFormClass.tour_name = self.toursTable.item(self.toursTable.currentRow(), 1).text()
                self.hide()
                self.tourOrderFormClass.show()

    def show_price_list(self):
        if len(self.toursTable.selectedItems()) == 1:
            self.priceListFormClass.tour_id = int(self.toursTable.item(self.toursTable.currentRow(), 0).text())
            self.hide()
            self.priceListFormClass.show()

    def delete_tour(self):
        if len(self.toursTable.selectedItems()) == 1:
            tour_id = self.toursTable.item(self.toursTable.currentRow(), 0).text()
            self.dBaser.delete_data("tours", tour_id)
            try:
                fill_table(self.toursTable, self.dBaser)
            except ErrorClass as e:
                e.show_error_message(self)

    def five_star_hotels(self):
        if len(self.toursTable.selectedItems()) == 1:
            self.returnBut.setEnabled(True)
            tour_id = self.toursTable.item(self.toursTable.currentRow(), 0).text()
            self.tourInfoTe.setVisible(True)
            info = f"Пятизвездочные отели в туре \"{self.toursTable.item(self.toursTable.currentRow(), 1).text()}\":\n"
            hotels = self.dBaser.get_five_star_hotels(tour_id)
            if len(hotels) != 0:
                info += "Населенный пункт\tНазвание отеля\n"
                for hotel in hotels:
                    info += f"{self.dBaser.inxs_to_points[hotel[0]]}\t\t{hotel[1]}\n"
            else:
                info += "Отсутствуют пятизвездочные отели по маршруту данного тура\n"
            self.tourInfoTe.setText(info)

    def show_tour_info(self):
        if len(self.toursTable.selectedItems()) == 1:
            self.returnBut.setEnabled(True)
            tour_id = self.toursTable.item(self.toursTable.currentRow(), 0).text()
            self.tourInfoTe.setVisible(True)
            info = f"Информация о туре: \"{self.toursTable.item(self.toursTable.currentRow(), 1).text()}\"\n"
            tour_points = self.dBaser.get_tour_points(tour_id)
            info += "Тип тура: " + self.toursTable.item(self.toursTable.currentRow(), 2).text() + "\n"
            info += "Место отправления: " + self.toursTable.item(self.toursTable.currentRow(), 3).text() + "\n"
            info += "Тип транспорта: " + self.toursTable.item(self.toursTable.currentRow(), 4).text() + "\n"
            info += "Общее число заказов: " + self.toursTable.item(self.toursTable.currentRow(), 5).text() + "\n"
            if len(tour_points) != 0:
                tour_points = ", ".join([self.dBaser.inxs_to_points[point[0]] for point in tour_points])
                info += "Населеные пункты тура: " + tour_points
            else:
                info += "Населенные пункты в туре пока отсутствуют\n"
            price_lists = self.todBaser.get_price_list(tour_id)
            start_dates, end_dates, prices = price_list_producing(price_lists)
            if len(start_dates) != 0:
                info += "\nПрайс листы на данный тур:\n"
                info += "Дата начала\tДата конца\tЦена\n"
                for i in range(len(start_dates)):
                    info += f"{start_dates[i]}\t{end_dates[i]}\t{prices[i]}\n"
            else:
                info += "Прайс листы на данный тур отсутствуют"
            info += info_note
            self.tourInfoTe.setText(info)

    def return_to_tours(self):
        self.tourInfoTe.clear()
        self.tourInfoTe.setVisible(False)
        self.returnBut.setEnabled(False)


def fill_table(table: QtWidgets.QTableWidget, dbaser: DBaser):
    labels = dbaser.get_table_headers("tours")
    labels = [cols_names_rus[name] for name in labels]
    data = dbaser.get_table_data("tours")
    if len(data) == 0:
        table.clear()
        table.setColumnCount(0)
        table.setRowCount(0)
        raise ErrorClass("Отсутствуют данные для отображения!")
    table.setColumnCount(len(labels))
    table.setHorizontalHeaderLabels(labels)

    header = table.horizontalHeader()
    max_size = max([len(x) for x in labels])
    header.setDefaultSectionSize(max_size * 9)

    rows_count = len(data)
    table.setRowCount(rows_count)
    for row in range(rows_count):
        for column in range(len(labels)):
            if column == 2:
                table.setItem(row, column, QtWidgets.QTableWidgetItem(str(dbaser.inxs_to_tour_types[data[row][column]])))
            elif column == 3:
                table.setItem(row, column, QtWidgets.QTableWidgetItem(str(dbaser.inxs_to_points[data[row][column]])))
            elif column == 4:
                table.setItem(row, column, QtWidgets.QTableWidgetItem(str(dbaser.inxs_to_transp[data[row][column]])))
            else:
                table.setItem(row, column, QtWidgets.QTableWidgetItem(str(data[row][column])))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = ToursFormClass("../../" + path_to_db)
    MainWindow.show()
    sys.exit(app.exec_())
