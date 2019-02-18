from django.urls import path
from . import views

urlpatterns = [
    path('search/<str:word>/', views.entry_point),
    path('delete/<str:word>/', views.delete_point),
    path('list/', views.BooksList.as_view()),
    path('list/<int:pk>', views.BooksDetail.as_view())
]