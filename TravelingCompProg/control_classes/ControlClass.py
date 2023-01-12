from forms import MainFormClass, DataChangeFormClass, ToursFormClass, NewTourClass


class FormsManager:

    def __init__(self):
        self.mainForm = MainFormClass()
        self.dataChangeFormClass = DataChangeFormClass()
        self.toursFormClass = ToursFormClass()
        self.newTourClass = NewTourClass()

        self.mainForm.changeDataBut.clicked.connect(self.show_data_change_form)
        self.mainForm.exitBut.clicked.connect(lambda: self.mainForm.close())
        self.mainForm.allToursBut.clicked.connect(self.show_tours_form)

        self.dataChangeFormClass.backBut.clicked.connect(self.back_from_data_change)

        self.toursFormClass.backBut.clicked.connect(self.back_from_forms)
        self.toursFormClass.addTourBut.clicked.connect(self.show_create_tour_form)

        self.newTourClass.backBut.clicked.connect(self.hide_create_tour_form)

    def start(self):
        self.mainForm.show()

    def show_data_change_form(self):
        self.mainForm.hide()
        self.dataChangeFormClass.show()

    def back_from_data_change(self):
        self.mainForm.show()
        self.dataChangeFormClass.hide()

    def show_tours_form(self):
        self.mainForm.hide()
        self.toursFormClass.show()

    def back_from_forms(self):
        self.mainForm.show()
        self.toursFormClass.hide()

    def show_create_tour_form(self):
        self.newTourClass.show()
        self.toursFormClass.hide()

    def hide_create_tour_form(self):
        self.newTourClass.hide()
        self.toursFormClass.show()


if __name__ == "__main__":
    pass
