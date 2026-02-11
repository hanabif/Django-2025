from rest_framework import serializers
from .models import Author,Book

class BookSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source = 'author.name', read_only = True)

    class Meta:
        model = Book
        fields = '__all__'

class AuthorSerializer(serializers.ModelSerializer):
    books = serializers.StringRelatedField(many = True)

    class Meta:
        model = Author
        fields = '__all__'

class BookTitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ["title"]


class TopAuthorSerializer(serializers.ModelSerializer):
    total_revenue = serializers.DecimalField(max_digits=10, decimal_places=2)
    books = BookTitleSerializer(many=True)

    class Meta:
        model = Author
        fields = ["id", "name", "total_revenue", "books"]