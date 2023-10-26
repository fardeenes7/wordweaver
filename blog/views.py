from django.shortcuts import render, redirect

# Create your views here.

from django.shortcuts import render, get_object_or_404
from .models import Post, Category, Tag, PostView, Comment, Bookmark
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


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    PostView.objects.create(post=post)
    if request.method == 'POST':
        try:
            if request.POST.get('body'):
                Comment.objects.create(
                    post = post,
                    user = request.user if request.user.is_authenticated else None,
                    body = request.POST.get('comment')
                )
                messages.success(request, 'Comment submitted successfully.')
            elif request.POST.get('action') == 'add_bookmark':
                Bookmark.objects.create(post=post, user=request.user)
                messages.success(request, 'Bookmark added')
            elif request.POST.get('action') == 'remove_bookmark':
                Bookmark.objects.get(post=post, user=request.user).delete()
                messages.success(request, 'Bookmark Removed')
        except:
            messages.error(request, 'Something went wrong.')
        return redirect('post_detail', slug=post.slug)
    context = {
        'post': post,
        'related_posts': Post.objects.filter(category=post.category).exclude(slug=post.slug)[:4],
        'comments': post.comment.all(),
        'is_bookmarked': True if request.user.is_authenticated and Bookmark.objects.filter(post=post, user=request.user).exists() else False
    }
    return render(request, 'blog/post_detail.html', context)


def category_list(request):
    context = {
        'categories': Category.objects.all()
    }
    return render(request, 'blog/category/list.html', context)


def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    posts = Post.objects.filter(category=category).filter(status='Published')
    context = {
        'category': category,
        'posts': posts,
    }
    return render(request, 'blog/category/detail.html', context)


