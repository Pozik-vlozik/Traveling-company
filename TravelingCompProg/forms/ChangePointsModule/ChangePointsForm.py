from ChangePointsClass import Ui_ChangePointsform
from dbaser import path_to_db, ErrorClass
from ChangePointsDBaser import CHPDBaser
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QMessageBox
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import Qt


class ChangePointsFormClass(QMainWindow, Ui_ChangePointsform):

    def __init__(self, path=path_to_db, parent=None):
        super(ChangePointsFormClass, self).__init__()
        self.setupUi(self)
        self.path = path
        self.parent = parent
        self.tour_id = 12
        self.dBaser = CHPDBaser(path)
        self.msgBox = QMessageBox()

        self.backBut.clicked.connect(self.back_to_tours)
        self.changePointsBut.clicked.connect(self.change_vis_points)

    def showEvent(self, a0: QtGui.QShowEvent) -> None:
        if self.tour_id != -1:
            self.set_points()

    def hideEvent(self, a0: QtGui.QHideEvent) -> None:
        self.del_ch_boxes()

    def del_ch_boxes(self):
        for widget in self.scrollAreaWidgetContents.children():
            if isinstance(widget, QtWidgets.QCheckBox):
                widget.deleteLater()

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

    def set_points(self):
        points = [x for x in self.dBaser.points_to_inxs.keys()]
        if len(points) == 0:
            self.msg_box("Внимание!", "Сначала добавте города!")
            return
        for i in range(len(points)):
            self.add_check_box(0, i, points[i])
        vis_points = self.dBaser.get_visit_points(self.tour_id)
        vis_points = [point[0] for point in vis_points]
        self.set_visited_points(vis_points)

    def set_visited_points(self, vis_points: list):
        if len(vis_points) != 0:
            for widget in self.scrollAreaWidgetContents.children():
                if isinstance(widget, QtWidgets.QCheckBox):
                    if self.dBaser.points_to_inxs[widget.objectName()] in vis_points:
                        widget.setCheckState(Qt.Checked)

    def get_checked_points(self):
        checked_points = []
        for widget in self.scrollAreaWidgetContents.children():
            if isinstance(widget, QtWidgets.QCheckBox):
                if widget.isChecked():
                    checked_points.append(self.dBaser.points_to_inxs[widget.objectName()])
        return checked_points

    def add_check_box(self, column: int, row: int, label: str):
        self.checkBox = QtWidgets.QCheckBox(self.scrollAreaWidgetContents)
        self.checkBox.setObjectName(label)
        self.gridLayout.addWidget(self.checkBox, row, column, 1, 1)
        self.checkBox.setText(label)

    def change_vis_points(self):
        self.dBaser.del_tour_points(self.tour_id)
        checked_points = self.get_checked_points()
        if len(checked_points) != 0:
            try:
                self.dBaser.set_tour_points(self.tour_id, checked_points)
                self.back_to_tours()
            except ErrorClass as e:
                e.show_error_message(self)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = ChangePointsFormClass("../../" + path_to_db)
    MainWindow.show()
    sys.exit(app.exec_())
