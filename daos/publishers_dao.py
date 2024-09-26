from daos.dao import DAO


class PublisherDAO(DAO):
    def read_by_id(self, publisher_id):
        query = "SELECT name FROM publishers WHERE publisher_id = %s"
        self.cursor.execute(query, (publisher_id,))
        result = self.cursor.fetchone()
        return result['name'] if result else None
