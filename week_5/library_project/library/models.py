from django.db import models

# Create your models here.

class Author(models.Model):
    name = models.CharField(max_length= 100)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length= 50)

    def __str__(self):
        return self.name
    
class Book(models.Model):
    title = models.CharField(max_length= 200)
    isbn = models.CharField(max_length=13, unique=True)
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name='books'
    )
    categories = models.ManyToManyField(
        Category,
        related_name='books'
    )
    total_copies = models.PositiveBigIntegerField()
    available_copies = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.title

class Member(models.Model):
    name = models.CharField(max_length= 100)
    email = models.EmailField(unique=True)
    joined_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class Loan(models.Model):
    book = models.ForeignKey(
        Book,
        on_delete= models.CASCADE,
        related_name= 'loans'
    )
    member = models.ForeignKey(
        Member,
        on_delete= models.CASCADE,
        related_name= 'loans'
    )
    loan_date = models.DateField(auto_now_add=True)
    return_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.book.title} -> {self.member.name}"