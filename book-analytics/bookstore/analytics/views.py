from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Book, Author
from .serializers import AuthorSerializer, BookSerializer,TopAuthorSerializer
from django.db.models import Q,Sum, Prefetch,Value,DecimalField
from django.db.models.functions import Coalesce
# Create your views here.

# 1a - Books published after 2010
class BooksAfter2010(APIView):
    def get(self, request):
        books = Book.objects.filter(published_year__gt = 2010)
        serializer = BookSerializer(books, many = True)
        return Response(serializer.data)

# 1b - Title contains Python
class PythonBooks(APIView):
    def get(self, request):
        books = Book.objects.filter(title__icontains = 'python')
        serializer = BookSerializer(books, many = True)
        return Response(serializer.data)

# 1c - Authors from USA sorted
class USAAuthors(APIView):
    def get(self, request):
        authors = Author.objects.filter(country = 'USA').order_by('name')
        serializer = AuthorSerializer(authors, many = True)
        return Response(serializer.data)

# 2d - Efficient books with author (select_related)
class BooksWithAuthors(APIView):
    def get(self, request):
        books = Book.objects.select_related('author')
        serializer = BookSerializer(books, many = True)
        return Response(serializer.data)

# 2e - Authors with books (prefetch_related)
class AuthorsWithBooks(APIView):
    def get(self, request):
        authors = Author.objects.prefetch_related("books")
        serializer = AuthorSerializer(authors, many=True)
        return Response(serializer.data)

# 3f - Books price > 0 and valid 13-digit ISBN
class ValidPaidBooks(APIView):
    def get(self, request):
        books = Book.objects.filter(
            price__gt = 0,
            isbn__regex = r'^\d{13}$'
        )
        serializer = BookSerializer(books, many = True)
        return Response(serializer.data)

# 3g - Authors with at least one book > $50
class AuthorsWithExpensiveBooks(APIView):
    def get(self, request):
        authors = Author.objects.filter(
            books__price__gt=50
        ).distinct()
        serializer = AuthorSerializer(authors, many=True)
        return Response(serializer.data)
    

#bonus
class TopAuthorsByRevenue(APIView):
    def get(self, request):
        top_authors = (
            Author.objects
            .annotate(
                total_revenue=Coalesce(
                    Sum('books__price'),
                    Value(0),
                    output_field=DecimalField(max_digits=10, decimal_places=2)
                )
            )
            .order_by('-total_revenue')[:5]
            .prefetch_related(
                Prefetch(
                    'books',
                    queryset=Book.objects.only('title')
                )
            )
        )

        serializer = TopAuthorSerializer(top_authors, many=True)
        return Response(serializer.data)
