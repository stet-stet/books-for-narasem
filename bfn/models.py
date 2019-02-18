from django.db import models


# Create your models here.
class Keyword(models.Model):
    word = models.CharField(max_length=100)
    count = models.IntegerField()


class Books(models.Model):
    isbn = models.CharField(max_length=30)
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=60)
    publisher = models.CharField(max_length=40)
    year = models.CharField(max_length=10)
    price = models.CharField(max_length=10)
    keyword = models.CharField(max_length=10)


class FailedBooks(models.Model):
    isbn = models.CharField(max_length=30)
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=60)
    keyword = models.CharField(max_length=30)