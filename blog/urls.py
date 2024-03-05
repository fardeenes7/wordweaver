from django.urls import path, include
from .views import *

urlpatterns = [
    path('category/all', category_list, name='category_list'),
    path('category/<str:slug>/', category_detail, name='category_detail'),

    path('tags/', tag_list, name='tag_list'),
    path('tags/<str:slug>/', tag_detail, name='tag_detail'),

    path('search/', search, name='search'),
    
    path('<str:slug>/', post_detail, name='post_detail'),

    path('comment/<int:id>/delete/', comment_delete, name='comment_delete'),

]