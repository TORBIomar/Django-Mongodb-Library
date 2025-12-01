from django.contrib import admin
from django.urls import path
from library import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.book_list, name='book_list'),
    path('search/', views.book_search, name='book_search'),  # Add this line
]