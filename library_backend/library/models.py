from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    user_type = models.CharField(max_length=10) 

class Book(models.Model):
    name = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    publication_year = models.IntegerField()