from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.db.models import Count
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from .forms import LoginForm, RegisterForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import authenticate, login, logout
from django.db.models import Count, Q
from django.contrib.auth.decorators import login_required

#Model imports
from blog.models import Post, Category, Tag
from user.models import Profile, Follow

def index(request):
    categories = []
    
    for cat in Category.objects.annotate(published_post_count=Count('post', filter=Q(post__status='Published'))).filter(published_post_count__gt=0).order_by('name'):
        categories.append({
            'category': cat,
            'posts': Post.objects.filter(category=cat).order_by('-created_at')[:3],
        })
    context = {
        'categories': categories,
        'slider_posts': Post.objects.filter(status='Published').order_by('-created_at')[:3],
        'latest_posts': Post.objects.filter(status='Published').order_by('-created_at')[:12],
    }
    return render(request, 'index/index.html', context)


def latest_posts(request):
    posts = Post.objects.filter(status='Published').order_by('-created_at')
    paginator = Paginator(posts, 12)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    context = {
        'posts': posts,
    }
    return render(request, 'blog/latest_posts.html', context)



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
            'author': User.objects.get(username=username).profile,
            'user': User.objects.get(username=username),
            'posts': Post.objects.filter(author__username=username, status='Published').order_by('-created_at'),
            'is_followed': Follow.objects.filter(follower=request.user, following__username=username).exists()
        }
    except Exception as e:
        print(e)
        context = {
            'author': None
        }
    return render(request, 'author/profile.html', context)


def follow_author(request, username):
    try:
        author = User.objects.get(username=username)
        follow = Follow.objects.create(follower=request.user, following=author)
        messages.success(request, f"Followed {author.profile}")
    except Exception as e:
        print(e)
        messages.error(request, "Something went wrong")
    return redirect ('author_profile', username=username)


def unfollow_author(request, username):
    try:
        author = User.objects.get(username=username)
        follow = Follow.objects.get(follower=request.user, following=author)
        follow.delete()
        messages.success(request, f"Unfollowed {author.profile}")
    except:
        messages.error(request, "Something went wrong")
    return redirect ('author_profile', username=username)






from .newsletter import newsletter_email

@login_required
def send_newsletter(request):
    if request.user.is_superuser:
        newsletter_email()
        messages.success(request, 'Newsletter sent successfully')
        return HttpResponseRedirect(reverse('admin:index'))
    else:
        messages.error(request, 'You are not authorized to send newsletter')
    return HttpResponseRedirect(reverse('index'))


from user.models import Subscriber
def newsletter_subscribe(request):
    email = request.POST.get('email-address')
    if email:
        Subscriber.objects.create(email=email)
        messages.success(request, 'Subscribed to newsletter successfully')

    return HttpResponseRedirect(reverse('index'))



def about(request):
    return render(request, 'extra/about.html')


def privacy(request):
    return render(request, 'extra/privacy.html')


def terms(request):
    return render(request, 'extra/terms.html')