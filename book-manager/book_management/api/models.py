from django.db import models

# Create your models here.
class Author(models.Model):
    name = models.CharField(max_length=200)
    bio = models.TextField(blank = True, null = True)
    date_of_birth = models.DateField(blank = True, null = True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'authors'
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def to_dict(self):
        return{
            'id': self.id,
            'name': self.name,
            'bio': self.bio,
            'date_of_birth': self.date_of_birth.isoformat() if self.date_of_birth else None,
            'created_at': self.created_at.isoformat()
        }

class Category(models.Model):
    name = models.CharField(max_length = 100, unique = True)

    class Meta:
        db_table = 'categories'
        verbose_name_plural = 'categories'
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def to_dict(self):
        return{
            'id': self.id,
            'name': self.name,
        }

class Book(models.Model):
    title = models.CharField(max_length = 300)
    author = models.ForeignKey(
        Author,
        on_delete = models.CASCADE,
        related_name = 'books'
    )
    published_date = models.DateField(blank=True, null=True)
    isbn = models.CharField(max_length=13, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField(
        Category,
        related_name='books',
        blank=True
    )

    class Meta:
        db_table = 'books'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def to_dict(self, include_author=True, include_categories=True):
        data = {
            'id': self.id,
            'title': self.title,
            'author_id': self.author_id,
            'published_date': self.published_date.isoformat() if self.published_date else None,
            'isbn': self.isbn,
            'price': str(self.price),
            'available': self.available,
            'created_at': self.created_at.isoformat()
        }

        if include_author:
            data['author'] = self.author.to_dict()
        if include_categories:
            data['categories'] = [cat.to_dict() for cat in self.categories.all()]
        
        return data
    
