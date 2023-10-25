from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, get_object_or_404
from .models import Post, Category, Tag
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count
from django.views.generic import ListView, DetailView
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import PostForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.utils import timezone

# Create your views here.

def index(request):
    post_list = Post.objects.all()
    paginator = Paginator(post_list, 5)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    context = {
        'posts': posts,
    }
    return render(request, 'index/index.html', context)