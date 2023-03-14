from django.urls import path
from user_auth import views

urlpatterns = [
    path('signup/', views.RegistrationAPIView.as_view(), name='signup'),
    path('login/', views.LoginAPIView.as_view(), name='login'),
    path('logout/', views.LogoutAPIView.as_view(), name='logout'),
]