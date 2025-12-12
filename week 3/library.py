class Library:
    def __init__(self):
        self.books = []

    def add_book(self, title):
        self.books.append(title)

    def show_books(self):
        for b in self.books:
            print(b)

lib = Library()
lib.add_book("Python Basics")
lib.add_book("Data Structures")
lib.show_books()
