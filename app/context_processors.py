from blog.models import Category, Post, Tag
from django.contrib.auth.models import User

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
