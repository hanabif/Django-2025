# api/views/author_views.py

import json
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db.models import Count
from datetime import datetime
from api.models import Author


@method_decorator(csrf_exempt, name='dispatch')
class AuthorListView(View):
    def get(self, request):
        authors = Author.objects.all()
        data = [author.to_dict() for author in authors]
        return JsonResponse({
            'success': True,
            'count': len(data),
            'data': data
        }, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class AuthorDetailView(View):
    def get(self, request, id):
        try:
            author = Author.objects.get(id=id)
            return JsonResponse({
                'success': True,
                'data': author.to_dict()
            }, status=200)
        except Author.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': f'Author with id {id} not found'
            }, status=404)


@method_decorator(csrf_exempt, name='dispatch')
class AuthorCreateView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            
            if 'name' not in data or not data['name'].strip():
                return JsonResponse({
                    'success': False,
                    'error': 'Name is required'
                }, status=400)
            
            date_of_birth = None
            if 'date_of_birth' in data and data['date_of_birth']:
                try:
                    
                    date_of_birth = datetime.strptime(data['date_of_birth'], '%Y-%m-%d').date()
                except ValueError:
                    return JsonResponse({
                        'success': False,
                        'error': 'Invalid date format. Use YYYY-MM-DD'
                    }, status=400)
                
            author = Author.objects.create(
                name=data['name'].strip(),
                bio=data.get('bio', ''),
                date_of_birth=date_of_birth
            )
            
            return JsonResponse({
                'success': True,
                'message': 'Author created successfully',
                'data': author.to_dict()
            }, status=201)
            
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
class AuthorUpdateView(View):
    def put(self, request, id):
        try:
            author = Author.objects.get(id=id)
            data = json.loads(request.body)
            
            if 'name' in data:
                author.name = data['name'].strip()
            if 'bio' in data:
                author.bio = data['bio']
            if 'date_of_birth' in data:
                if data['date_of_birth']:
                    try:
                        author.date_of_birth = datetime.strptime(data['date_of_birth'], '%Y-%m-%d').date()
                    except ValueError:
                        return JsonResponse({
                            'success': False,
                            'error': 'Invalid date format. Use YYYY-MM-DD'
                        }, status=400)
                else:
                    author.date_of_birth = None
            
            author.save()
            
            return JsonResponse({
                'success': True,
                'message': 'Author updated successfully',
                'data': author.to_dict()
            }, status=200)
            
        except Author.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': f'Author with id {id} not found'
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
class AuthorDeleteView(View):
    def delete(self, request, id):
        try:
            author = Author.objects.get(id=id)
            author_name = author.name
            author.delete()
            
            return JsonResponse({
                'success': True,
                'message': f'Author "{author_name}" deleted successfully'
            }, status=200)
            
        except Author.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': f'Author with id {id} not found'
            }, status=404)


@method_decorator(csrf_exempt, name='dispatch')
class AuthorBooksView(View):
    def get(self, request, id):
        try:
            author = Author.objects.get(id=id)
            
            books = author.books.prefetch_related('categories').all()
            
            data = [book.to_dict(include_author=False) for book in books]
            
            return JsonResponse({
                'success': True,
                'author': author.to_dict(),
                'book_count': len(data),
                'books': data
            }, status=200)
            
        except Author.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': f'Author with id {id} not found'
            }, status=404)


@method_decorator(csrf_exempt, name='dispatch')
class AuthorBookCountView(View):
    def get(self, request):
        
        authors = Author.objects.annotate(
            book_count=Count('books')
        ).order_by('-book_count')
        
        data = []
        for author in authors:
            author_dict = author.to_dict()
            author_dict['book_count'] = author.book_count
            data.append(author_dict)
        
        return JsonResponse({
            'success': True,
            'count': len(data),
            'data': data
        }, status=200)