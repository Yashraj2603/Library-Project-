from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login,name='login'),
    path('home/', views.home , name='home'),
    path('addBook/', views.add_book, name='addBook'),
    path('deleteBook/', views.delete_book, name='deleteBook'),
]
