from django.urls import path

from user_auth.views import RegistrationAPIView, LoginAPIView, LogoutAPIView

urlpatterns = [
    path('signup/', RegistrationAPIView.view_as, name='signup'),
    path('login/', LoginAPIView.view_as, name='login'),
    path('logout/', LogoutAPIView.view_as, name='logout'),
]