from django.urls import path
from . import views

app_name = 'books'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('books/', views.my_library_view, name='my_library'),
    path('books/add/', views.book_add_view, name='book_add'),
    path('books/edit/<int:pk>/', views.book_edit_view, name='book_edit'),
    path('books/delete/<int:pk>/', views.book_delete_view, name='book_delete'),
    path('books/toggle-public/<int:pk>/', views.book_toggle_public_view, name='book_toggle_public'),
    path('books/discover/', views.discover_view, name='discover'),
    path('books/<int:pk>/', views.book_detail_view, name='book_detail'),
]
