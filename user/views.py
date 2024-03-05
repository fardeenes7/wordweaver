from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from blog.forms import PostForm
from blog.models import Post, Category, Tag
from .models import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required


@login_required
def profile(request):
    context = {
        'profile': User.objects.get(username=request.user.username).profile,
        'post_count': Post.objects.filter(author=request.user).filter(status='Published').count(),
    }
    return render(request, 'user/profile/profile.html', context)


@login_required
def profile_edit(request):
    if request.method == 'POST':
        try:
            user = request.user
            user.first_name = request.POST.get('first_name')
            user.last_name = request.POST.get('last_name')
            user.username = request.POST.get('username')
            user.email = request.POST.get('email')
            if request.FILES.get('image'):
                user.profile.image = request.FILES.get('image')
                user.profile.save()
            user.save()
            messages.success(request, 'Profile updated successfully')
        except Exception as e:
            print(e)
            messages.error(request, 'Something went wrong')
        return redirect('my_profile_edit')

    return render(request, 'user/profile/edit.html')


@login_required
def following(request):
    context = {
        'followings': Follow.objects.filter(follower=request.user)
    }
    return render(request, 'user/following.html', context)


@login_required
def followers(request):
    context = {
        'followers': Follow.objects.filter(following=request.user)
    }
    return render(request, 'user/followers.html', context)


@login_required
def post_list(request):
    post_list = Post.objects.filter(author=request.user).order_by('-created_at')
    if request.GET.get('status'):
        post_list = post_list.filter(status=request.GET.get('status'))
    if request.GET.get('category'):
        post_list = post_list.filter(category__slug=request.GET.get('category'))
    context = {
        'posts': post_list,
    }
    return render(request, 'user/post/list.html', context)


@login_required
def post_create(request):
    form = PostForm()
    if request.method == 'POST':
        post = Post.objects.create(
            title=request.POST.get('title'),
            body=request.POST['body'],
            category=Category.objects.get(id=request.POST['category']),
            image = request.FILES.get('image'),
            author = request.user,
            status = 'Pending' if request.POST.get('publish') == 'yes' else 'Draft'
        )
        tag_list =request.POST.get('tags').split(',')
        for tag in tag_list:
            post.tags.add(Tag.objects.get_or_create(name=tag.strip())[0])
        return redirect('my_post_edit', slug=post.slug)
    context = {
        'form': form
    }
    return render(request, 'user/post/create.html', context)


@login_required
def post_edit(request, slug):
    post = Post.objects.get(slug=slug)
    if request.method == 'POST':
        post.title = request.POST.get('title')
        post.body = request.POST.get('body')
        post.category = Category.objects.get(id=request.POST['category'])
        post.image = request.FILES.get('image') if request.FILES.get('image') else post.image
        post.status = 'Pending' if request.POST.get('publish') == 'yes' else 'Draft'
        post.tags.clear()
        post.save()
        tag_list =request.POST.get('tags').split(',')
        for tag in tag_list:
            post.tags.add(Tag.objects.get_or_create(name=tag.strip())[0])
        post.save()
        return redirect('my_post_edit', slug=post.slug)
    context = {
        'post': post,
        'tag_string': ', '.join([tag.name for tag in post.tags.all()]),
        'form': PostForm(instance=post)
    }
    return render(request, 'user/post/edit.html', context)


@login_required
def post_delete(request, slug):
    try:
        post = Post.objects.get(slug=slug)
        if post.author != request.user:
            raise Exception('You are not allowed to delete this post')
        post.delete()
        messages.success(request, 'Post deleted successfully')
        return redirect('my_post_list')
    except Exception as e:
        messages.error(request, str(e))
        return redirect('my_post_edit', slug=slug)



@login_required
def bookmarks(request):
    context = {
        'posts': Post.objects.filter(bookmark__user=request.user).order_by('-bookmark__created_at')
    }
    return render(request, 'user/bookmarks.html', context)


@login_required
def settings(request):
    context = {
        'newsletter': Subscriber.objects.filter(email=request.user.email).exists(),
        'new_post_alert': request.user.profile.new_post_email,
    }
    return render(request, 'user/settings.html', context)


@login_required
def newsletter_toggle(request):
    print(request.POST)
    if request.POST.get('newsletter') == 'on':
        Subscriber.objects.get_or_create(email=request.user.email)
        messages.success(request, 'Subscribed to newsletter successfully')
    else:
        try:
            Subscriber.objects.get(email=request.user.email).delete()
            messages.success(request, 'Unsubscribed from newsletter successfully')
        except:
            messages.error(request, 'Something went wrong')
    return redirect('my_settings')


def new_post_alert_toggle(request):
    print(request.POST)
    if request.POST.get('new_post_alert') == 'on':
        request.user.profile.new_post_email = True
        request.user.profile.save()
        messages.success(request, 'Subscribed to new post alerts successfully')
    else:
        try:
            request.user.profile.new_post_email = False
            request.user.profile.save()
            messages.success(request, 'Unsubscribed from new post alerts successfully')

        except:
            messages.error(request, 'Something went wrong')
    return redirect('my_settings')