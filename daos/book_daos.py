from daos.dao import DAO
from models.book import Book

class BookDAO(DAO):
    def read_all(self):
        query = "SELECT * FROM books"
        self.cursor.execute(query)
        results = self.cursor.fetchall()
        return [Book(**result) for result in results]
