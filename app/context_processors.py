from blog.models import Category, Post, Tag
from django.contrib.auth.models import User
from django.db.models import Count, F
from django.utils import timezone
from datetime import timedelta


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

def get_most_viewed_posts():
    # Calculate the date 30 days ago from today
    thirty_days_ago = timezone.now() - timedelta(days=3)

    # Filter posts that have at least one view in the last 30 days
    posts = Post.objects.filter(view__date__gte=thirty_days_ago)

    posts = posts.annotate(views_in_last_30_days=Count('view')).filter(view__date__gte=thirty_days_ago)

    # Order the posts by views in the last 30 days in descending order
    posts = posts.order_by('-views_in_last_30_days')[:5]
    return posts

def blog_data(request):
    data = {
        'trending_post_list': get_most_viewed_posts(),
    }
    return data