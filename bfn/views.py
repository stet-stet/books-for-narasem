from django.shortcuts import render
from rest_framework.views import APIView
from bfn.models import Books, FailedBooks
from bfn.serializers import BooksSerializer, FailedBooksSerializer
from django.http import Http404
from rest_framework.response import Response
from rest_framework import status
from bfn.scraputil.Entry import get_results_from_API
from bfn.scraputil.Kyobo import bookinfo_from_kyobo
from bfn.scraputil.Narasem import search_narasem


# Create your views here.

def entry_point(request, keyword):
    search_res = get_results_from_API()
    for i in search_res[:]:
        try:
            Books.objects.get(isbn=repr(i["isbn"]))
            search_res.remove(i)
        except:
            continue;

    entries = []
    for i in search_res[:]:
        s = bookinfo_from_kyobo(i["isbn"])
        if s is None:
            search_res.remove(i)
        else:
            entries.append(s)

    for i in entries[:]:
        if not search_narasem(i["title"], i["author"], i["year"]):
            entries.remove(i)

    for i in entries[:]:
        i["keyword"] = keyword
        Books.objects.create(i)


def delete_point(request, word):
    try:
        Books.objects.filter(keyword=word).delete()
    except:
        pass


class BooksList(APIView):
    """
    List all eligible books, or make a new book.
    """
    def get(self, request, format=None):
        books = Books.objects.all()
        serializer = BooksSerializer(books, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = BooksSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BooksDetail(APIView):
    """
    Retrieve/update/delete a snippet instance
    """

    def get_object(self, pk):
        try:
            return Books.objects.get(pk=pk)
        except Books.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = BooksSerializer(snippet)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        book = self.get_object(pk)
        serializer = BooksSerializer(book)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        book = self.get_object(pk)
        book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
