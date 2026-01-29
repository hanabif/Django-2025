from django.contrib import admin
from .models import Author, Book, Mmeber, Category, Loan

# Register your models here.
admin.site.register(Author)
admin.site.register(Member)
admin.site.register(Category)
admin.site.register(Loan)

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'available_copies')
    list_filter = ('author', 'categories')
    search_fields = ('title', 'isbn')