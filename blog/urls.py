from django.urls import path, include
from .views import *

urlpatterns = [
    path('<str:slug>/', post_detail, name='post_detail'),
    path('category/all', category_list, name='category_list'),
    path('category/<str:slug>/', category_detail, name='category_detail'),


    

]