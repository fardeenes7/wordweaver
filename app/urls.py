from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('login/', Login.as_view(), name='login'),
    path('register/', Register, name='register'),
    path('logout/', Logout, name='logout'),

    path('author/', author_list, name='author_list'),
    path('author/all', author_list, name='author_list'),
    path('author/<str:username>', author_profile, name='author_profile'),
]