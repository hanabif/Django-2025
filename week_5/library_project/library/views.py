from django.shortcuts import render
from .models import Book, Member, Loan
from django.http import JsonResponse
from django.views import View
# Create your views here.

def book_list(request):
    books = Book.objects.select_related('author').prefetch_related('categories')

    data = []
    for book in books:
        data.append({
            'title': book.title,
            'author': book.author.name,
            'categories': [c.name for c in book.categories.all()],
            'available_copies': book.available_copies,
        })
    return JsonResponse(data, safe = False)


class CreateLoanView(View):
    def post(self, request, book_id):
        member_id = request.POST.get('member_id')

        book = get_object_or_404(Book, id = book_id)
        member = get_object_or_404(Member, id = member_id)

        if book.availabe_copies <= 0:
            return JsonResponse({'error': 'Book not available'}, status = 400)
        
        Loan.objects.create(book=book, member=member)
        book.available_copies -= 1
        book.save()

        return JsonResponse({'message': 'Loan created successfully'})