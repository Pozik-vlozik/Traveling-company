from temp import path_to_db, cols_names_rus
from error_class import ErrorClass
from PyQt5 import QtWidgets
import sqlite3 as sq


class DBaser:

    def __init__(self, path=path_to_db):
        self.path = path
        try:
            self.connection = sq.connect(self.path)
            self.cur = self.connection.cursor()
            self.cur.execute("PRAGMA foreign_keys = ON")
            self.cur.execute("PRAGMA case_sensitive_like = true;")
        except Exception:
            raise ErrorClass("Ошибка в открытии базы данных!")
        self.points_to_inxs = {}
        self.inxs_to_points = {}
        self.tour_types_to_inxs = {}
        self.inxs_to_tour_types = {}
        self.transp_to_inxs = {}
        self.inxs_to_transp = {}
        self.update_dicts()

    def update_dicts(self):
        self.cur.execute("SELECT * FROM points")
        self.points_to_inxs = {point[1]: point[0] for point in self.cur.fetchall()}
        self.inxs_to_points = {v: k for k, v in self.points_to_inxs.items()}

        self.cur.execute("SELECT * FROM tour_types")
        self.tour_types_to_inxs = {point[1]: point[0] for point in self.cur.fetchall()}
        self.inxs_to_tour_types = {v: k for k, v in self.tour_types_to_inxs.items()}

        self.cur.execute("SELECT * FROM transport_types")
        self.transp_to_inxs = {point[1]: point[0] for point in self.cur.fetchall()}
        self.inxs_to_transp = {v: k for k, v in self.transp_to_inxs.items()}

    def get_table_names(self):
        self.cur.execute("SELECT * FROM sqlite_master WHERE TYPE = 'table'")
        t_names = [tname[1] for tname in self.cur.fetchall()]
        return t_names

    def get_table_headers(self, tableName: str):
        self.cur.execute("PRAGMA table_info({})".format(tableName))
        col_names = [tname[1] for tname in self.cur.fetchall()]
        return col_names

    def get_table_data(self, tableName: str, sortingBy=None, limit=0, WHERE=None):
        query = "SELECT * FROM {} ".format(tableName)
        if WHERE is not None:
            query += WHERE
        if sortingBy is not None:
            query += " ORDER BY {} ".format(sortingBy)
        if limit != 0:
            query += " LIMIT {} ".format(limit)
        self.cur.execute(query)
        data = self.cur.fetchall()
        return data

    def get_hotels(self, where=None):
        query = f"""SELECT hotel_id, point_name, name, stars 
                    FROM hotels h 
                    JOIN points p ON h.point_id = p.point_id """
        if where is not None:
            query += where
        self.cur.execute(query)
        return self.cur.fetchall()

    def change_data(self, tableName: str, data: list, index: int):
        query = "UPDATE {} SET ".format(tableName)
        values = ["'" + str(val) + "'" for val in data]
        headers = self.get_table_headers(tableName)
        updated_columns = []
        line_id = headers[0]
        for val in zip(headers, values):
            updated_columns.append(val[0] + "=" + val[1])
        query += ", ".join(updated_columns)
        query += " WHERE {}={}".format(line_id, index)
        try:
            self.cur.execute(query)
            self.connection.commit()
        except Exception:
            raise ErrorClass("Некорректно введенные данные!")

    def delete_data(self, tableName: str, index: int):
        row_id = self.get_table_headers(tableName)[0]
        query = "DELETE FROM {} WHERE {}={}".format(tableName, row_id, index)
        self.cur.execute(query)
        self.connection.commit()

    def add_data(self, tableName: str, data: list):
        cols = self.get_table_headers(tableName)
        cols = ", ".join([col for col in cols[1:]])
        values = ", ".join(["'" + str(dat) + "'" for dat in data])
        query = f"INSERT INTO {tableName} ({cols}) VALUES ({values})"
        try:
            self.cur.execute(query)
            self.connection.commit()
        except Exception:
            raise ErrorClass("Некорректно введенные данные!")

    def get_tour_points(self, tour_id: int):
        query = f"SELECT point_id FROM tour_points WHERE tour_id={tour_id}"
        self.cur.execute(query)
        data = self.cur.fetchall()
        return data

    def get_five_star_hotels(self, tour_id: int):
        query = f"""SELECT hotels.point_id, hotels.name
                    FROM hotels  
                    WHERE point_id IN  
                        (SELECT point_id 
                        FROM tour_points 
                        WHERE tour_id = {tour_id} AND stars=5)"""
        self.cur.execute(query)
        hotels = self.cur.fetchall()
        return hotels

    def get_all_tours(self):
        query = "SELECT tour_id FROM tours"
        self.cur.execute(query)
        return self.cur.fetchall()

    def get_tour_name(self, tour_id: int):
        query = f"SELECT tour_name FROM tours WHERE tour_id={tour_id}"
        self.cur.execute(query)
        return self.cur.fetchall()


def fill_table(tableName: str, table: QtWidgets.QTableWidget, dBaser: DBaser):
    labels = dBaser.get_table_headers(tableName)
    labels = [cols_names_rus[name] for name in labels]
    data = dBaser.get_table_data(tableName)
    if len(data) == 0:
        raise ErrorClass("Отсутствуют данные для отображения!")
    custome_fill_table(table, data, labels)


def custome_fill_table(table: QtWidgets.QTableWidget, data: list, labels: list):
    table.setColumnCount(len(labels))
    table.setHorizontalHeaderLabels(labels)

    header = table.horizontalHeader()
    max_size = max([len(x) for x in labels])
    header.setDefaultSectionSize(max_size * 9)

    rows_count = len(data)
    table.setRowCount(rows_count)
    for row in range(rows_count):
        for column in range(len(labels)):
            table.setItem(row, column, QtWidgets.QTableWidgetItem(str(data[row][column])))
