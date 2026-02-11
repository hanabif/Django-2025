from django.urls import path
from .views import (
    BooksAfter2010,
    PythonBooks,
    USAAuthors,
    BooksWithAuthors,
    AuthorsWithBooks,
    ValidPaidBooks,
    AuthorsWithExpensiveBooks,
    TopAuthorsByRevenue
)

urlpatterns = [
    path("books/after-2010/", BooksAfter2010.as_view()),
    path("books/python/", PythonBooks.as_view()),
    path("authors/usa/", USAAuthors.as_view()),
    path("books/with-authors/", BooksWithAuthors.as_view()),
    path("authors/with-books/", AuthorsWithBooks.as_view()),
    path("books/valid-paid/", ValidPaidBooks.as_view()),
    path("authors/expensive/", AuthorsWithExpensiveBooks.as_view()),
    path("authors/top-revenue/", TopAuthorsByRevenue.as_view()),

]