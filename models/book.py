class Book:
    def __init__(self, book_id, title, summary, publication_date, pages, isbn, price, author_id, publisher_id):
        self.book_id = book_id
        self.title = title
        self.summary = summary
        self.publication_date = publication_date
        self.pages = pages
        self.isbn = isbn
        self.price = price
        self.author_id = author_id
        self.publisher_id = publisher_id

    def __repr__(self):
        return f"livre : {self.title}"
