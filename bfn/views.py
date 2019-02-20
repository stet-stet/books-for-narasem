from django.shortcuts import render
from rest_framework.views import APIView
from bfn.models import Books, FailedBooks
from bfn.serializers import BooksSerializer, FailedBooksSerializer
from django.http import Http404
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework import status
from bfn.scraputil.Entry import get_results_from_API
from bfn.scraputil.Kyobo import bookinfo_from_kyobo
from bfn.scraputil.Narasem import search_narasem
from rest_framework import viewsets, permissions
from rest_framework_csv import renderers as r
from rest_framework.settings import api_settings

# Create your views here.

def entry_point(request, key_word):
    try:
        search_res = get_results_from_API(key_word)
    except KeyboardInterrupt:
        return None
    except:
        return HttpResponse("something bad happened with the API.")

    try:
        for i in search_res[:]:
            try:
                Books.objects.get(isbn=i["isbn"])
                search_res.remove(i)
            except:
                continue;
    except KeyboardInterrupt:
        return None
    except:
        return HttpResponse("something bad happened with the API when parsing.")

    entries = []
    for i in search_res[:]:
        try:
            s = bookinfo_from_kyobo(i["isbn"])
        except KeyboardInterrupt:
            return
        except:
            return HttpResponse("kyobo")
        if s is None:
            search_res.remove(i)
        else:
            entries.append(s)
    print("*********after kyobo: " + repr(len(entries)))
    for i in range(5):
        print(entries[i])
    for i in entries[:]:
        try:
            if search_narasem(i["title"], i["author"], i["year"]):
                print("removed!")
                entries.remove(i)
        except KeyboardInterrupt:
            return HttpResponse("Narasem.")
        except KeyError:
            print("A keyerror has occurred!")
            entries.remove(i)
        except:
            return HttpResponse("Narasem.")
    print("*********after narasem: "+repr(len(entries)))
    for i in entries[:]:
        i["keyword"] = key_word
        print(i)
        try:
            Books.objects.create(**i)
        except:
            return HttpResponse("That last bit!")

    return HttpResponse("All is done and well. keyword:"+repr(key_word)+","+repr(len(entries)))


def delete_point(request, key_word):
    try:
        Books.objects.filter(keyword=key_word).delete()
    except:
        pass
    return HttpResponse("all with keyword "+repr(key_word)+" is well deleted")


# class BooksList(APIView):
#     """
#     List all eligible books, or make a new book.
#     """
#     def get(self, request, format=None):
#         books = Books.objects.all()
#         serializer = BooksSerializer(books, many=True)
#         return Response(serializer.data)
#
#     def post(self, request, format=None):
#         serializer = BooksSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# class BooksDetail(APIView):
#     """
#     Retrieve/update/delete a snippet instance
#     """
#
#     def get_object(self, pk):
#         try:
#             return Books.objects.get(pk=pk)
#         except Books.DoesNotExist:
#             raise Http404
#
#     def get(self, request, pk, format=None):
#         snippet = self.get_object(pk)
#         serializer = BooksSerializer(snippet)
#         return Response(serializer.data)
#
#     def put(self, request, pk, format=None):
#         book = self.get_object(pk)
#         serializer = BooksSerializer(book)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def delete(self, request, pk, format=None):
#         book = self.get_object(pk)
#         book.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

class BooksViewSet(viewsets.ModelViewSet):
    queryset = Books.objects.all()
    serializer_class = BooksSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    renderer_classes = (r.CSVRenderer,) + tuple(api_settings.DEFAULT_RENDERER_CLASSES)
