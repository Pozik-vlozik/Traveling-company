import sqlite3 as sq
from temp import path_to_db


def main():
    with sq.connect(path_to_db) as con:
        cur = con.cursor()

        # cur.execute("""DROP TABLE IF EXISTS tour_types""")
        # cur.execute("""CREATE TABLE tour_types (
        #                 type_id INTEGER PRIMARY KEY AUTOINCREMENT,
        #                 type_name STRING NOT NULL
        #                 )""")
        #
        # cur.execute("""DROP TABLE IF EXISTS transport_types""")
        # cur.execute("""CREATE TABLE transport_types (
        #                 type_id INTEGER PRIMARY KEY AUTOINCREMENT,
        #                 type_name STRING NOT NULL
        #                 )""")

        cur.execute("""DROP TABLE IF EXISTS points""")
        cur.execute("""CREATE TABLE points (
                        point_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        point_name STRING NOT NULL UNIQUE
                        )""")

        # cur.execute("""DROP TABLE IF EXISTS tour_points""")
        # cur.execute("""CREATE TABLE tour_points (
        #                 string_id INTEGER PRIMARY KEY AUTOINCREMENT,
        #                 tour_id INTEGER NOT NULL,
        #                 point_id INTEGER NOT NULL,
        #                 FOREIGN KEY (tour_id)
        #                     REFERENCES tours(tour_id)
        #                     ON DELETE CASCADE
        #                 FOREIGN KEY (point_id)
        #                     REFERENCES points(point_id)
        #                     ON DELETE CASCADE
        #                 )""")
        #
        # cur.execute("""DROP TABLE IF EXISTS hotels""")
        # cur.execute("""CREATE TABLE hotels (
        #                 hotel_id INTEGER PRIMARY KEY AUTOINCREMENT,
        #                 point_id INTEGER NOT NULL,
        #                 name STRING NOT NULL,
        #                 stars INTEGER DEFAULT NULL,
        #                 FOREIGN KEY (point_id)
        #                     REFERENCES points(point_id)
        #                     ON DELETE CASCADE
        #                 CHECK (stars BETWEEN 0 AND 5)
        #                 )""")
        #
        # cur.execute("""DROP TABLE IF EXISTS price_list""")
        # cur.execute("""CREATE TABLE price_list (
        #                 list_id INTEGER PRIMARY KEY AUTOINCREMENT,
        #                 tour_id INTEGER NOT NULL,
        #                 start_date DATE NOT NULL,
        #                 finish_date DATE NOT NULL,
        #                 price INTEGER NOT NULL
        #                 CHECK (start_date <= finish_date AND
        #                         price >= 0),
        #                 FOREIGN KEY (tour_id)
        #                     REFERENCES tours(tour_id)
        #                     ON DELETE CASCADE
        #                 )""")
        #
        # cur.execute("""DROP TABLE IF EXISTS tours""")
        # cur.execute("""CREATE TABLE tours (
        #                 tour_id INTEGER PRIMARY KEY AUTOINCREMENT,
        #                 tour_name STRING NOT NULL,
        #                 tour_type INTEGER NOT NULL,
        #                 departure_point STRING NOT NULL,
        #                 transport_type INTEGER NOT NULL,
        #                 orders_amount INTEGER NOT NULL,
        #                 FOREIGN KEY (tour_type)
        #                     REFERENCES tour_types(type_id)
        #                     ON DELETE CASCADE
        #                 FOREIGN KEY (transport_type)
        #                     REFERENCES transport_types(type_id)
        #                     ON DELETE CASCADE
        #                 )""")


if __name__ == "__main__":
    main()
