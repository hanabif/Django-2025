from django.contrib import admin
from .models import Author, Book, Category
# Register your models here.


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'date_of_birth', 'created_at']
    search_fields = ['name']
    list_filter = ['created_at']
    ordering = ['name']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']
    ordering = ['name']


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'author', 'isbn', 'price', 'available', 'published_date']
    search_fields = ['title', 'isbn', 'author__name']
    list_filter = ['available', 'categories', 'published_date']
    filter_horizontal = ['categories']
    ordering = ['-created_at']