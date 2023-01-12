from dbaser import DBaser, path_to_db


class ChangeDBaser(DBaser):

    def __init__(self, path=path_to_db):
        super(ChangeDBaser, self).__init__(path)

    def get_points(self):
        query = "SELECT point_name FROM points"
        self.cur.execute(query)
        points = self.cur.fetchall()
        return points

