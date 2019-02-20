from rest_framework import serializers
from bfn.models import Books, FailedBooks


class BooksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Books
        fields = ('isbn', 'title', 'author', 'publisher', 'year', 'price', 'keyword')


class FailedBooksSerializer(serializers.ModelSerializer):
    class Meta:
        model = FailedBooks
        fields = ('isbn', 'title', 'author', 'keywords')
