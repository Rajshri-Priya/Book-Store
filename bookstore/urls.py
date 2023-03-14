"""bookstore URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

# Define the schema view for Swagger
schema_view = get_schema_view(
    openapi.Info(
        title="BOOK STORE",
        default_version='v1',
        description="Book Store api helps to create, update, delete fxnality for books.",
        # terms_of_service="https://terms/services",
        contact=openapi.Contact(email="priyagorkha711@gmail.com"),
        # license=openapi.License(name="License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
    # Set csrf_cookie=True to include a CSRF cookie for Swagger UI
    # to include the CSRF token in requests.
    # csrf_cookie=True,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('user_auth.urls')),
    path('books/', include('book.urls')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

]
