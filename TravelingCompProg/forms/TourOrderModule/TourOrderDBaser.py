from dbaser import DBaser, path_to_db


class TODBaser(DBaser):

    def __init__(self, path=path_to_db):
        super(TODBaser, self).__init__(path)

    def get_price_list(self, tour_id: int):
        query = f"SELECT * FROM price_list WHERE tour_id={tour_id}"
        self.cur.execute(query)
        price_lists = self.cur.fetchall()
        return price_lists

    def inc_orders_amount(self, tour_id: int):
        query = f"UPDATE tours SET orders_amount = orders_amount + 1 WHERE tour_id = {tour_id}"
        self.cur.execute(query)
        self.connection.commit()

    def get_tours_names(self):
        query = f"""SELECT group_concat(tour_name, ', ') FROM tours;"""
        self.cur.execute(query)
        return self.cur.fetchall()[0][0]


def price_list_producing(price_list: list):
    start_dates = []
    end_dates = []
    prices = []
    for note in price_list:
        start_dates.append(note[2])
        end_dates.append(note[3])
        prices.append(note[4])

    return start_dates, end_dates, prices


if __name__ == "__main__":
    db = TODBaser("..\\..\\" + path_to_db)
    print(db.get_tours_names())
