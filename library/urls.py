from django.urls import path
from . import views

urlpatterns = [
    path('', views.book_list, name='book_list'),  # Add this line for the root URL
    path('search/', views.book_search, name='book_search'),
    path('book/<str:book_id>/', views.book_detail, name='book_detail'),
]