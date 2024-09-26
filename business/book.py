from daos.book_daos import BookDAO
from daos.authors_dao import AuthorDAO
from daos.publishers_dao import PublisherDAO


def get_all_books():
    book_dao = BookDAO()
    author_dao = AuthorDAO()
    publisher_dao = PublisherDAO()

    books = book_dao.read_all()
    print("Books fetched:", books)
    for book in books:
        book.author_name = author_dao.read_by_id(book.author_id)
        book.publisher_name = publisher_dao.read_by_id(book.publisher_id)

    return books
