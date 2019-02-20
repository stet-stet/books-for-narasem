from django.urls import path,include
from . import views
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'list', views.BooksViewSet)


urlpatterns = [
    path('',include(router.urls)),
    path('search/<str:key_word>/', views.entry_point),
    path('delete/<str:key_word>/', views.delete_point),
]
