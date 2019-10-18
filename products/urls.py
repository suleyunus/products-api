from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import (
    ProductsView
)

urlpatterns = [
    path('authtoken/', obtain_auth_token),
    path('products/', ProductsView.as_view()),
]