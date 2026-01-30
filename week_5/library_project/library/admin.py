from django.contrib import admin
from .models import Author, Book, Member, Category, Loan

# Register your models here.
admin.site.register(Author)
admin.site.register(Member)
admin.site.register(Category)
admin.site.register(Loan)

class AvailabilityFilter(admin.SimpleListFilter):
    title = 'availability'
    parameter_name = 'availability'

    def lookups(self, request, model_admin):
        return (
            ('available', 'Available'),
            ('unavailable', 'Unavailable'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'available':
            return queryset.filter(available_copies__gt=0)
        if self.value() == 'unavailable':
            return queryset.filter(available_copies=0)
        return queryset

class AuthorFilter(admin.SimpleListFilter):
    title = 'author'
    parameter_name = 'author'

    def lookups(self, request, model_admin):
        return [(str(a.id), a.name) for a in Author.objects.order_by('name')]

    def queryset(self, request, queryset):
        if self.value():
            try:
                author_id = int(self.value())
            except (TypeError, ValueError):
                return queryset
            return queryset.filter(author_id=author_id)
        return queryset

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'available_copies')
    list_filter = (AuthorFilter, 'categories')
    search_fields = ('title', 'isbn')