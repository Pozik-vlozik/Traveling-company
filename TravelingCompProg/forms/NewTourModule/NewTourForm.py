from NewTourClass import Ui_TourCreateForm
from PyQt5.QtWidgets import QMainWindow
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QMessageBox
from dbaser import DBaser, path_to_db, ErrorClass


class NewTourClass(QMainWindow, Ui_TourCreateForm):

    def __init__(self, path=path_to_db):
        super(NewTourClass, self).__init__()
        self.setupUi(self)
        self.dBaser = DBaser(path)
        self.createTourBut.clicked.connect(self.create_tour)
        self.msgBox = QMessageBox()

    def showEvent(self, a0: QtGui.QShowEvent) -> None:
        self.dBaser.update_dicts()
        self.fill_combo_boxes()

    def fill_combo_boxes(self):
        self.tourTypeCb.clear()
        for value in self.dBaser.tour_types_to_inxs.keys():
            self.tourTypeCb.addItem(value)
        self.departPointCb.clear()
        for value in self.dBaser.points_to_inxs.keys():
            self.departPointCb.addItem(value)
        self.transpTypeCb.clear()
        for value in self.dBaser.transp_to_inxs.keys():
            self.transpTypeCb.addItem(value)

    def msg_box(self, title: str, text: str, icon=None):
        self.msgBox.setText(text)
        self.msgBox.setWindowTitle(title)
        if icon is not None:
            self.msgBox.setIcon(icon)
        self.msgBox.exec()

    def create_tour(self):
        tour_name = self.tourNameLe.text()
        if tour_name == "":
            self.msg_box("Внимание!", "Заполните поле названия тура!")
            return
        tour_type = self.dBaser.tour_types_to_inxs[self.tourTypeCb.currentText()]
        depart_point = self.dBaser.points_to_inxs[self.departPointCb.currentText()]
        transp_type = self.dBaser.transp_to_inxs[self.transpTypeCb.currentText()]
        try:
            self.dBaser.add_data("tours", [tour_name, tour_type, depart_point, transp_type, 0])
            self.tourNameLe.clear()
            self.msg_box("Успех!", "Вы успешно создали тур!")
        except ErrorClass as e:
            e.show_error_message(self)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = NewTourClass("../../" + path_to_db)
    MainWindow.show()
    sys.exit(app.exec_())
