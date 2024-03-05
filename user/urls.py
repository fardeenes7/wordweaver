from django.urls import path, include
from .views import *

urlpatterns = [
    path('', profile, name='my_profile'),
    path('edit/', profile_edit, name='my_profile_edit'),
    path('post/all/', post_list, name='my_post_list'),
    path('post/create/', post_create, name='my_post_create'),
    path('post/<str:slug>/', post_edit, name='my_post_edit'),
    path('post/<str:slug>/delete/', post_delete, name='my_post_delete'),
    path('settings/', settings, name='my_settings'),
    path('bookmarks/', bookmarks, name='my_bookmarks'),
    path('following/', following, name="my_following"),
    path('toggle/newsletter', newsletter_toggle, name='my_newsletter_toggle'),
    path('toggle/new_post_alert', new_post_alert_toggle, name='my_new_post_alert_toggle'),
    
]