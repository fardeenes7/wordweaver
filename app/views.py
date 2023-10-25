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

#Model imports
from blog.models import Post, Category, Tag
from user.models import Profile

def index(request):
    post_list = Post.objects.all().order_by('-created_at')
    paginator = Paginator(post_list, 5)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    context = {
        'posts': posts,
    }
    return render(request, 'index/index.html', context)



class Login(LoginView):
    template_name = 'auth/login.html'
    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect(reverse_lazy('user'))
        return super().dispatch(request, *args, **kwargs)


def Register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile = Profile.objects.create(user=user)
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