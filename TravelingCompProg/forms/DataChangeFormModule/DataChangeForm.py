from temp import path_to_db, table_names_eng, cols_names_rus, cols_names_eng
from DataChangeClass import Ui_ChangeDataWindow
from PyQt5.QtWidgets import QMainWindow
from PyQt5 import QtWidgets, QtGui
from dbaser import ErrorClass
from ChangeDBaser import ChangeDBaser


class DataChangeFormClass(QMainWindow, Ui_ChangeDataWindow):

    def __init__(self, path=path_to_db):
        super(DataChangeFormClass, self).__init__()
        self.setupUi(self)
        try:
            self.dBaser = ChangeDBaser(path)
        except ErrorClass as e:
            e.show_error_message(self)
        self.row_index_for_change = -1
        self.isHotels = False

        self.tableForChangeCB.currentTextChanged.connect(self.change_table_data)
        self.tableWidget.itemClicked.connect(self.row_selected)
        self.addDataBut.clicked.connect(self.add_data)
        self.deleteDataBut.clicked.connect(self.delete_data)
        self.changeDataBut.clicked.connect(self.change_data)
        self.searchLE.textChanged.connect(self.text_changed)

    def text_changed(self):
        cur_table = self.tableForChangeCB.currentText()
        labels = self.dBaser.get_table_headers(table_names_eng[cur_table])
        labels = [cols_names_rus[label] for label in labels]
        column = cols_names_eng[self.searchCB.currentText()]
        like = "%" + self.searchLE.text().lower() + "%"
        if cur_table != "Отели":
            data = self.dBaser.get_table_data(table_names_eng[cur_table],
                                              WHERE=f" WHERE ({column} LIKE '{like}')")
        else:
            data = self.dBaser.get_hotels(where=f" WHERE (LOWER({column}) LIKE '{like}')")
        custome_fill_table(self.tableWidget, data, labels)

    def showEvent(self, a0: QtGui.QShowEvent) -> None:
        if self.tableForChangeCB.currentText() == "Отели":
            self.fill_combo_box()
        fill_table(table_names_eng[self.tableForChangeCB.currentText()], self.tableWidget, self.dBaser, self.isHotels)

    def mousePressEvent(self, a0: QtGui.QMouseEvent) -> None:
        self.stackOfButs.setCurrentIndex(0)
        self.row_index_for_change = -1

    def fill_combo_box(self):
        points = self.dBaser.get_points()
        self.pointsCB.clear()
        for point in points:
            self.pointsCB.addItem(point[0])

    def change_data(self):
        values = []
        for widget in self.stackOfLEs.currentWidget().children():
            if isinstance(widget, QtWidgets.QLineEdit):
                values.append(widget.text())
            elif isinstance(widget, QtWidgets.QComboBox):
                values.append(self.dBaser.points_to_inxs[widget.currentText()])
        tableName = table_names_eng[self.tableForChangeCB.currentText()]
        values.insert(0, self.row_index_for_change)
        try:
            self.dBaser.change_data(tableName, values, self.row_index_for_change)
            fill_table(tableName, self.tableWidget, self.dBaser, self.isHotels)
            self.dBaser.update_dicts()
        except ErrorClass as e:
            e.show_error_message(self)
            return

    def add_data(self):
        values = []
        for widget in self.stackOfLEs.currentWidget().children():
            if isinstance(widget, QtWidgets.QLineEdit):
                values.append(widget.text())
            elif isinstance(widget, QtWidgets.QComboBox):
                values.append(self.dBaser.points_to_inxs[widget.currentText()])
        table_name = table_names_eng[self.tableForChangeCB.currentText()]
        try:
            self.dBaser.add_data(table_name, values)
            fill_table(table_name, self.tableWidget, self.dBaser, self.isHotels)
            self.dBaser.update_dicts()
        except ErrorClass as e:
            e.show_error_message(self)
            return
        self.clear_text()

    def row_selected(self):
        self.row_index_for_change = self.tableWidget.item(self.tableWidget.currentRow(), 0).text()
        values = []
        if self.tableForChangeCB.currentText() != "Отели":
            for i in range(self.tableWidget.columnCount()):
                values.append(self.tableWidget.item(self.tableWidget.currentRow(), i).text())
        else:
            for i in range(self.tableWidget.columnCount() - 1):
                values.append(self.tableWidget.item(self.tableWidget.currentRow(), i + 1).text())

        index = 1
        for widget in self.stackOfLEs.currentWidget().children():
            if isinstance(widget, QtWidgets.QLineEdit):
                widget.setText(values[index])
                index += 1
            elif isinstance(widget, QtWidgets.QComboBox):
                widget.setCurrentIndex(widget.findText(self.tableWidget.item(self.tableWidget.currentRow(), 1).text()))
        self.stackOfButs.setCurrentIndex(1)

    def delete_data(self):
        table_name = table_names_eng[self.tableForChangeCB.currentText()]
        try:
            self.dBaser.delete_data(table_name, self.row_index_for_change)
            fill_table(table_name, self.tableWidget, self.dBaser, self.isHotels)
            self.dBaser.update_dicts()
        except ErrorClass as e:
            e.show_error_message(self)
            return
        self.stackOfButs.setCurrentIndex(0)
        self.row_index_for_change = -1
        self.clear_text()

    def change_table_data(self):
        cur_text = self.tableForChangeCB.currentText()
        if cur_text == "Отели":
            self.isHotels = True
        else:
            self.isHotels = False
        try:
            if self.tableForChangeCB.currentText() == "Отели":
                self.fill_combo_box()
                custome_fill_table(self.tableWidget,
                                   self.dBaser.get_hotels(),
                                   [cols_names_rus[h] for h in self.dBaser.get_table_headers(table_names_eng[cur_text])])
            else:
                fill_table(table_names_eng[cur_text], self.tableWidget, self.dBaser, self.isHotels)
        except ErrorClass as e:
            e.show_error_message(self)
        self.searchCB.clear()
        labels = self.dBaser.get_table_headers(table_names_eng[cur_text])
        for label in labels[1::]:
            self.searchCB.addItem(cols_names_rus[label])
        self.stackOfLEs.setCurrentIndex(self.tableForChangeCB.findText(cur_text))
        self.stackOfButs.setCurrentIndex(0)
        self.row_index_for_change = -1
        self.clear_text()

    def clear_text(self):
        for widget in self.stackOfLEs.currentWidget().children():
            if isinstance(widget, QtWidgets.QLineEdit):
                widget.clear()


def fill_table(tableName: str, table: QtWidgets.QTableWidget, dBaser: ChangeDBaser, isHotel=False):
    data = dBaser.get_table_data(tableName)
    if len(data) == 0:
        table.setColumnCount(0)
        table.setRowCount(0)
        raise ErrorClass("Отсутствуют данные для отображения!")
    labels = dBaser.get_table_headers(tableName)
    labels = [cols_names_rus[name] for name in labels]

    custome_fill_table(table, data, labels, isHotel, dBaser)


def custome_fill_table(table: QtWidgets.QTableWidget, data: list, labels: list, isHotels=False,
                       dbaser: ChangeDBaser=None):
    table.setColumnCount(len(labels))
    table.setColumnHidden(0, True)
    table.setHorizontalHeaderLabels(labels)

    header = table.horizontalHeader()
    max_size = max([len(x) for x in labels])
    header.setDefaultSectionSize(max_size * 9)

    rows_count = len(data)
    table.setRowCount(rows_count)
    for row in range(rows_count):
        for column in range(len(labels)):
            if isHotels and column == 1:
                table.setItem(row, column, QtWidgets.QTableWidgetItem(str(dbaser.inxs_to_points[data[row][column]])))
                continue
            table.setItem(row, column, QtWidgets.QTableWidgetItem(str(data[row][column])))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = DataChangeFormClass("../../" + path_to_db)
    MainWindow.show()
    sys.exit(app.exec_())
