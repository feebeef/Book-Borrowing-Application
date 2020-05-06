from django.urls import path
from catalog import views


urlpatterns = [
	path('', views.home, name = 'home'),
	path('books?search', views.search, name = 'search'),
	path('books', views.books, name = 'books'),
	path('books/<str:pk>/', views.book_instance, name= 'instance'),
	path('books/<str:pk>/review/', views.review, name= 'review'),
	path('profile/', views.profile, name='profile'),
	path('books/search', views.suggest, name='suggest'),
]