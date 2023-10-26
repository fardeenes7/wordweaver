from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count
from django.views.generic import ListView, DetailView
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.utils import timezone
from .forms import LoginForm, RegisterForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import authenticate, login, logout
from django.db.models import Count, Q

#Model imports
from blog.models import Post, Category, Tag
from user.models import Profile

def index(request):
    context = {
        'categories': Category.objects.annotate(published_post_count=Count('post', filter=Q(post__status='Published'))).filter(published_post_count__gt=0)[:5],
        'slider_posts': Post.objects.filter(status='Published').order_by('-created_at')[:1],
        'latest_posts': Post.objects.filter(status='Published').order_by('-created_at')[:4],
    }
    return render(request, 'index/index.html', context)



class Login(LoginView):
    template_name = 'auth/login.html'
    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect(reverse_lazy('my_profile'))
        return super().dispatch(request, *args, **kwargs)


def Register(request):
    if request.user.is_authenticated:
        return redirect(reverse_lazy('my_profile'))
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
        else:
            messages.error(request, 'Error creating account')
    else:
        form = RegisterForm()
    context = {
        'form': form
    }
    return render(request, 'auth/register.html', context)


def Logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def author_list(request):
    context = {
        'authors': User.objects.annotate(published_post_count=Count('post', filter=Q(post__status='Published'))).filter(published_post_count__gt=0)
    }
    return render(request, 'author/list.html', context)


def author_profile(request, username):
    try:
        context = {
            'author': User.objects.get(username=username).profile
        }
    except:
        context = {
            'author': None
        }
    return render(request, 'author/profile.html', context)