from django.contrib import admin
from django.urls import path, include
from .views import *
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', index, name='index'),
    path('login/', Login.as_view(), name='login'),
    path('register/', Register, name='register'),
    path('logout/', Logout, name='logout'),

    path('author/', author_list, name='author_list'),
    path('author/all', author_list, name='author_list'),
    path('author/<str:username>', author_profile, name='author_profile'),
    path('author/<str:username>/follow', follow_author, name='follow_author'),
    path('author/<str:username>/unfollow', unfollow_author, name='unfollow_author'),
    
    
    path('email/newsletter/send', send_newsletter, name='send_newsletter'),

    path('email/newsletter/subscribe', newsletter_subscribe, name='newsletter_subscribe'),

    path('about/', about, name='about'),
    path('privacy/', privacy, name='privacy'),
    path('terms/', terms, name='terms'),

    path('reset_password/', auth_views.PasswordResetView.as_view(), name='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    



]