# book_library.py

class BookNotAvailableError(Exception):
    pass

class Book:
    def __init__(self, title, author, isbn):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.is_lent = False

    def __str__(self):
        return f"{self.title:<25} {self.author:<20} {self.isbn:<15} Physical"

class EBook(Book):
    def __init__(self, title, author, isbn, download_size):
        super().__init__(title, author, isbn)
        self.download_size = download_size

    def __str__(self):
        return f"{self.title:<25} {self.author:<20} {self.isbn:<15} eBook - {self.download_size}MB"

class Library:
    def __init__(self):
        self.books = []

    def add_book(self, book):
        self.books.append(book)

    def remove_book(self, isbn):
        self.books = [b for b in self.books if b.isbn != isbn]

    def lend_book(self, isbn):
        for book in self.books:
            if book.isbn == isbn and not book.is_lent:
                book.is_lent = True
                return book
        raise BookNotAvailableError("Book is not available or already lent.")

    def return_book(self, isbn):
        for book in self.books:
            if book.isbn == isbn and book.is_lent:
                book.is_lent = False
                return
        raise BookNotAvailableError("This book was not lent out.")

    def update_book(self, isbn, new_title, new_author, new_size=None):
        for book in self.books:
            if book.isbn == isbn:
                book.title = new_title
                book.author = new_author
                if isinstance(book, EBook) and new_size:
                    book.download_size = new_size
                return True
        return False

    def find_book(self, isbn):
        for book in self.books:
            if book.isbn == isbn:
                return book
        return None

    def __iter__(self):
        return (b for b in self.books if not b.is_lent)

    def books_by_author(self, author):
        return (b for b in self.books if b.author.lower() == author.lower())
