from django.shortcuts import get_object_or_404, render
from .models import Book, Category, Member, Loan
from django.http import JsonResponse
from django.views import View
from django.db.models import Count, Q
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

#Function-Based View (FBV)
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

#Class-Based View (CBV)
@method_decorator(csrf_exempt, name='dispatch')
class CreateLoanView(View):
    def post(self, request, book_id):
        member_id = request.POST.get('member_id')

        book = get_object_or_404(Book, id = book_id)
        member = get_object_or_404(Member, id = member_id)

        if book.available_copies <= 0:
            return JsonResponse({'error': 'Book not available'}, status = 400)
        
        Loan.objects.create(book=book, member=member)
        book.available_copies -= 1
        book.save()

        return JsonResponse({'message': 'Loan created successfully'})
    
# Advanced ORM Queries
def books_never_loaned(request):
    books = Book.objects.filter(loans__isnull = True)

    data = [book.title for book in books]
    return JsonResponse(data, safe=False)

#Science books by Isaac Newton
Book.objects.filter(
    categories__name = 'Science',
    author__name = 'Isaac Newton'
)

#Top 3 members with most active loans
Member.objects.annotate(
    active_loans = Count(
        'loans',
        filter = Q(loans__return_date__isnull = True)
    )
).order_by('-active_loans')[:3]

#Count books per category
Category.objects.annotate(
    book_count=Count('books')
)
