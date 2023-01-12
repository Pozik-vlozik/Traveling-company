from dbaser import DBaser, path_to_db


class CHPDBaser(DBaser):

    def __init__(self, path=path_to_db):
        super(CHPDBaser, self).__init__(path)

    def get_visit_points(self, tour_id: int):
        query = f"SELECT point_id FROM tour_points WHERE tour_id = {tour_id}"
        self.cur.execute(query)
        points = self.cur.fetchall()
        return points

    def del_tour_points(self, tour_id: int):
        query = f"DELETE FROM tour_points WHERE tour_id={tour_id}"
        self.cur.execute(query)
        self.connection.commit()

    def set_tour_points(self, tour_id: int, vis_points: list):
        if len(vis_points) != 0:
            for point in vis_points:
                self.add_data("tour_points", [tour_id, point])
