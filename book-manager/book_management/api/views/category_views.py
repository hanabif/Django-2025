# api/views/category_views.py

import json
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db import IntegrityError

from api.models import Category, Book


@method_decorator(csrf_exempt, name='dispatch')
class CategoryListView(View):
    
    def get(self, request):
        categories = Category.objects.all()
        data = [category.to_dict() for category in categories]
        
        return JsonResponse({
            'success': True,
            'count': len(data),
            'data': data
        }, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class CategoryDetailView(View):
    
    def get(self, request, id):
        try:
            category = Category.objects.get(id=id)
            
            return JsonResponse({
                'success': True,
                'data': category.to_dict()
            }, status=200)
            
        except Category.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': f'Category with id {id} not found'
            }, status=404)


@method_decorator(csrf_exempt, name='dispatch')
class CategoryCreateView(View):
    
    def post(self, request):
        try:
            data = json.loads(request.body)
            
            
            if 'name' not in data or not data['name'].strip():
                return JsonResponse({
                    'success': False,
                    'error': 'Name is required'
                }, status=400)
            
            
            if Category.objects.filter(name__iexact=data['name'].strip()).exists():
                return JsonResponse({
                    'success': False,
                    'error': 'A category with this name already exists'
                }, status=400)
            
            category = Category.objects.create(
                name=data['name'].strip()
            )
            
            return JsonResponse({
                'success': True,
                'message': 'Category created successfully',
                'data': category.to_dict()
            }, status=201)
            
        except json.JSONDecodeError:
            return JsonResponse({
                'success': False,
                'error': 'Invalid JSON data'
            }, status=400)
        except IntegrityError:
            return JsonResponse({
                'success': False,
                'error': 'A category with this name already exists'
            }, status=400)
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=400)


@method_decorator(csrf_exempt, name='dispatch')
class CategoryUpdateView(View):
    
    def put(self, request, id):
        try:
            category = Category.objects.get(id=id)
            data = json.loads(request.body)
            
            if 'name' in data:
                new_name = data['name'].strip()
                
                # Check for unique name (excluding current category)
                if Category.objects.filter(name__iexact=new_name).exclude(id=id).exists():
                    return JsonResponse({
                        'success': False,
                        'error': 'A category with this name already exists'
                    }, status=400)
                
                category.name = new_name
            
            category.save()
            
            return JsonResponse({
                'success': True,
                'message': 'Category updated successfully',
                'data': category.to_dict()
            }, status=200)
            
        except Category.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': f'Category with id {id} not found'
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
class CategoryDeleteView(View):
    
    def delete(self, request, id):
        try:
            category = Category.objects.get(id=id)
            category_name = category.name
            category.delete()
            
            return JsonResponse({
                'success': True,
                'message': f'Category "{category_name}" deleted successfully'
            }, status=200)
            
        except Category.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': f'Category with id {id} not found'
            }, status=404)


@method_decorator(csrf_exempt, name='dispatch')
class CategoryBooksView(View):
    
    def get(self, request, id):
        try:
            category = Category.objects.get(id=id)
            
            
            books = Book.objects.select_related('author').prefetch_related('categories').filter(
                categories=category
            )
            
            data = [book.to_dict() for book in books]
            
            return JsonResponse({
                'success': True,
                'category': category.to_dict(),
                'book_count': len(data),
                'books': data
            }, status=200)
            
        except Category.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': f'Category with id {id} not found'
            }, status=404)