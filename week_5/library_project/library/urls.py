from django.urls import path
from .views import book_list, CreateLoanView

urlpatterns = [
    path('books/', book_list, name = 'book-list'),
    path('books/<int:book_id>/loan/', CreateLoanView.as_view(), name = 'book-loan')
]