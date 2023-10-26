from blog.models import Category, Post, Tag
from django.contrib.auth.models import User
from django.db.models import Count, F


def all_category_list(request):
    data =  {
        'all_category_list': Category.objects.all().order_by('name')
    }
    return data

def admin_stats(request):
    data = {
        'total_posts': Post.objects.all().count(),
        'pending_posts': Post.objects.filter(status='Pending').count(),
        'flagged_posts': Post.objects.filter(status='Flagged').count(),
        'published_posts': Post.objects.filter(status='Published').count(),
    }
    return data

def blog_data(request):
    data = {
        'trending_post_list': Post.objects.filter(status='Published').annotate(view_count=Count('view')).order_by(F('view_count').desc())[:5],
    }
    return data