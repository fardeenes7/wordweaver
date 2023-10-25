from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('login/', Login.as_view(), name='login'),
    path('register/', Register, name='register'),
    path('logout/', Logout, name='logout'),
]