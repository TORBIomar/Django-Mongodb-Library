from django.urls import path
from . import views

urlpatterns = [
    path('', views.book_list, name='book_list'),  # Add this line for the root URL
    path('search/', views.book_search, name='book_search'),
]