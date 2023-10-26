from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from blog.forms import PostForm
from blog.models import Post, Category, Tag
from django.contrib import messages

def profile(request):
    context = {
        'profile': User.objects.get(username=request.user.username).profile
    }
    return render(request, 'user/profile/profile.html', context)


def profile_edit(request):
    return render(request, 'user/profile/edit.html')


def following(request):
    return render(request, 'user/following.html')


def followers(request):
    return render(request, 'user/followers.html')







def post_list(request):
    post_list = Post.objects.filter(author=request.user).order_by('-created_at')
    if request.GET.get('status'):
        post_list = post_list.filter(status=request.GET.get('status'))
    context = {
        'posts': post_list
    }
    return render(request, 'user/post/list.html', context)


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
    return render(request, 'user/post/delete.html')


def bookmarks(request):
    context = {
        'posts': Post.objects.filter(bookmark__user=request.user).order_by('-bookmark__created_at')
    }
    return render(request, 'user/bookmarks.html', context)


def settings(request):
    return render(request, 'user/settings.html')