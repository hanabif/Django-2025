# api/views/book_views.py

import json
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db import IntegrityError

from api.models import Book, Author, Category


@method_decorator(csrf_exempt, name='dispatch')
class BookListView(View):
    
    def get(self, request):
        books = Book.objects.select_related('author').prefetch_related('categories').all()
        data = [book.to_dict() for book in books]
        
        return JsonResponse({
            'success': True,
            'count': len(data),
            'data': data
        }, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class BookDetailView(View):
    
    def get(self, request, id):
        try:
            book = Book.objects.select_related('author').prefetch_related('categories').get(id=id)
            
            return JsonResponse({
                'success': True,
                'data': book.to_dict()
            }, status=200)
            
        except Book.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': f'Book with id {id} not found'
            }, status=404)


@method_decorator(csrf_exempt, name='dispatch')
class BookCreateView(View):
    
    def post(self, request):
        try:
            data = json.loads(request.body)
            
            
            required_fields = ['title', 'author_id', 'isbn', 'price']
            for field in required_fields:
                if field not in data:
                    return JsonResponse({
                        'success': False,
                        'error': f'{field} is required'
                    }, status=400)
            
            
            if Book.objects.filter(isbn=data['isbn']).exists():
                return JsonResponse({
                    'success': False,
                    'error': 'A book with this ISBN already exists'
                }, status=400)
            
            
            try:
                author = Author.objects.get(id=data['author_id'])
            except Author.DoesNotExist:
                return JsonResponse({
                    'success': False,
                    'error': f'Author with id {data["author_id"]} not found'
                }, status=404)
            
            
            book = Book.objects.create(
                title=data['title'].strip(),
                author=author,
                published_date=data.get('published_date'),
                isbn=data['isbn'],
                price=data['price'],
                available=data.get('available', True)
            )
            
            
            if 'category_ids' in data and isinstance(data['category_ids'], list):
                categories = Category.objects.filter(id__in=data['category_ids'])
                book.categories.set(categories)
            

            book = Book.objects.select_related('author').prefetch_related('categories').get(id=book.id)
            
            return JsonResponse({
                'success': True,
                'message': 'Book created successfully',
                'data': book.to_dict()
            }, status=201)
            
        except json.JSONDecodeError:
            return JsonResponse({
                'success': False,
                'error': 'Invalid JSON data'
            }, status=400)
        except IntegrityError:
            return JsonResponse({
                'success': False,
                'error': 'A book with this ISBN already exists'
            }, status=400)
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=400)


@method_decorator(csrf_exempt, name='dispatch')
class BookUpdateView(View):
    
    def put(self, request, id):
        try:
            book = Book.objects.get(id=id)
            data = json.loads(request.body)
            
           
            if 'title' in data:
                book.title = data['title'].strip()
            if 'published_date' in data:
                book.published_date = data['published_date']
            if 'price' in data:
                book.price = data['price']
            if 'available' in data:
                book.available = data['available']
            
            
            if 'isbn' in data:
                if Book.objects.filter(isbn=data['isbn']).exclude(id=id).exists():
                    return JsonResponse({
                        'success': False,
                        'error': 'A book with this ISBN already exists'
                    }, status=400)
                book.isbn = data['isbn']
            
            
            if 'author_id' in data:
                try:
                    author = Author.objects.get(id=data['author_id'])
                    book.author = author
                except Author.DoesNotExist:
                    return JsonResponse({
                        'success': False,
                        'error': f'Author with id {data["author_id"]} not found'
                    }, status=404)
            
            book.save()
            
            
            if 'category_ids' in data:
                if isinstance(data['category_ids'], list):
                    categories = Category.objects.filter(id__in=data['category_ids'])
                    book.categories.set(categories)
            
            
            book = Book.objects.select_related('author').prefetch_related('categories').get(id=id)
            
            return JsonResponse({
                'success': True,
                'message': 'Book updated successfully',
                'data': book.to_dict()
            }, status=200)
            
        except Book.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': f'Book with id {id} not found'
            }, status=404)
        except json.JSONDecodeError:
            return JsonResponse({
                'success': False,
                'error': 'Invalid JSON data'
            }, status=400)
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=400)


@method_decorator(csrf_exempt, name='dispatch')
class BookDeleteView(View):
    
    def delete(self, request, id):
        try:
            book = Book.objects.get(id=id)
            book_title = book.title
            book.delete()
            
            return JsonResponse({
                'success': True,
                'message': f'Book "{book_title}" deleted successfully'
            }, status=200)
            
        except Book.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': f'Book with id {id} not found'
            }, status=404)



@method_decorator(csrf_exempt, name='dispatch')
class BooksByAuthorView(View):
    
    def get(self, request, author_id):
        try:
            author = Author.objects.get(id=author_id)
            books = Book.objects.select_related('author').prefetch_related('categories').filter(
                author_id=author_id
            )
            data = [book.to_dict() for book in books]
            
            return JsonResponse({
                'success': True,
                'author': author.to_dict(),
                'count': len(data),
                'data': data
            }, status=200)
            
        except Author.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': f'Author with id {author_id} not found'
            }, status=404)


@method_decorator(csrf_exempt, name='dispatch')
class BooksByCategoryView(View):
    
    def get(self, request, category_id):
        try:
            category = Category.objects.get(id=category_id)
            books = Book.objects.select_related('author').prefetch_related('categories').filter(
                categories__id=category_id
            )
            data = [book.to_dict() for book in books]
            
            return JsonResponse({
                'success': True,
                'category': category.to_dict(),
                'count': len(data),
                'data': data
            }, status=200)
            
        except Category.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': f'Category with id {category_id} not found'
            }, status=404)


@method_decorator(csrf_exempt, name='dispatch')
class BookSearchView(View):
    
    def get(self, request):
        query = request.GET.get('q', '').strip()
        
        if not query:
            return JsonResponse({
                'success': False,
                'error': 'Search query "q" is required'
            }, status=400)
        
        books = Book.objects.select_related('author').prefetch_related('categories').filter(
            title__icontains=query
        )
        data = [book.to_dict() for book in books]
        
        return JsonResponse({
            'success': True,
            'query': query,
            'count': len(data),
            'data': data
        }, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class BookPriceRangeView(View):
    
    def get(self, request):
        min_price = request.GET.get('min')
        max_price = request.GET.get('max')
        
        
        books = Book.objects.select_related('author').prefetch_related('categories')
        
        if min_price:
            try:
                books = books.filter(price__gte=float(min_price))
            except ValueError:
                return JsonResponse({
                    'success': False,
                    'error': 'Invalid min price value'
                }, status=400)
        
        if max_price:
            try:
                books = books.filter(price__lte=float(max_price))
            except ValueError:
                return JsonResponse({
                    'success': False,
                    'error': 'Invalid max price value'
                }, status=400)
        
        data = [book.to_dict() for book in books]
        
        return JsonResponse({
            'success': True,
            'filters': {
                'min_price': min_price,
                'max_price': max_price
            },
            'count': len(data),
            'data': data
        }, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class AvailableBooksView(View):
    
    def get(self, request):
        books = Book.objects.select_related('author').prefetch_related('categories').filter(
            available=True
        )
        data = [book.to_dict() for book in books]
        
        return JsonResponse({
            'success': True,
            'count': len(data),
            'data': data
        }, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class BooksOrderByDateView(View):
    
    def get(self, request):
        
        order = request.GET.get('order', 'asc')
        
        books = Book.objects.select_related('author').prefetch_related('categories')
        
        if order == 'desc':
            books = books.order_by('-published_date')
        else:
            books = books.order_by('published_date')
        
        data = [book.to_dict() for book in books]
        
        return JsonResponse({
            'success': True,
            'order': order,
            'count': len(data),
            'data': data
        }, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class Top5BooksView(View):
    
    def get(self, request):
        books = Book.objects.select_related('author').prefetch_related('categories').all()[:5]
        data = [book.to_dict() for book in books]
        
        return JsonResponse({
            'success': True,
            'count': len(data),
            'data': data
        }, status=200)