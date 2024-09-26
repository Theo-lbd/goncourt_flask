from daos.dao import DAO


class AuthorDAO(DAO):
    def read_by_id(self, author_id):
        query = "SELECT name FROM authors WHERE author_id = %s"
        self.cursor.execute(query, (author_id,))
        result = self.cursor.fetchone()
        return result['name'] if result else None
