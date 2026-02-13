
from django.urls import path
from . import views

urlpatterns = [
    
    path('authors/', views.AuthorListView.as_view(), name='author-list'),
    path('authors/book-count/', views.AuthorBookCountView.as_view(), name='author-book-count'),
    path('authors/create/', views.AuthorCreateView.as_view(), name='author-create'),
    path('authors/<int:id>/', views.AuthorDetailView.as_view(), name='author-detail'),
    path('authors/<int:id>/update/', views.AuthorUpdateView.as_view(), name='author-update'),
    path('authors/<int:id>/delete/', views.AuthorDeleteView.as_view(), name='author-delete'),
    path('authors/<int:id>/books/', views.AuthorBooksView.as_view(), name='author-books'),
  

    
    path('books/', views.BookListView.as_view(), name='book-list'),
    path('books/<int:id>/', views.BookDetailView.as_view(), name='book-detail'),
    path('books/create/', views.BookCreateView.as_view(), name='book-create'),
    path('books/<int:id>/update/', views.BookUpdateView.as_view(), name='book-update'),
    path('books/<int:id>/delete/', views.BookDeleteView.as_view(), name='book-delete'),
    
    
    path('books/author/<int:author_id>/', views.BooksByAuthorView.as_view(), name='books-by-author'),
    path('books/category/<int:category_id>/', views.BooksByCategoryView.as_view(), name='books-by-category'),
    path('books/search/', views.BookSearchView.as_view(), name='book-search'),
    path('books/price-range/', views.BookPriceRangeView.as_view(), name='book-price-range'),
    path('books/available/', views.AvailableBooksView.as_view(), name='books-available'),
    path('books/order-by-date/', views.BooksOrderByDateView.as_view(), name='books-order-by-date'),
    path('books/top-5/', views.Top5BooksView.as_view(), name='books-top-5'),

   
    path('categories/', views.CategoryListView.as_view(), name='category-list'),
    path('categories/<int:id>/', views.CategoryDetailView.as_view(), name='category-detail'),
    path('categories/create/', views.CategoryCreateView.as_view(), name='category-create'),
    path('categories/<int:id>/update/', views.CategoryUpdateView.as_view(), name='category-update'),
    path('categories/<int:id>/delete/', views.CategoryDeleteView.as_view(), name='category-delete'),
    path('categories/<int:id>/books/', views.CategoryBooksView.as_view(), name='category-books'),
]