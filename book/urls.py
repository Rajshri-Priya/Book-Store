from django.urls import path
from book import views
urlpatterns = [
    path('book_app/', views.BookAPI.as_view(), name='book'),
    path('book_app/<int:pk>', views.BookAPI.as_view(), name='book'),

]