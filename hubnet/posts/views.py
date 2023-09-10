from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from .models import Group, Post, User
from .forms import PostForm


def index(request):
    posts = Post.objects.order_by('-pub_date')
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = Post.objects.filter(group=group).order_by('-pub_date')[:10]
    group_name = group.title
    context = {
        'group': group,
        'posts': posts,
        'group_name': group_name,
    }
    return render(request, 'posts/group_list.html', context)


def post_detail(request, post_id):
    current_post = get_object_or_404(Post, pk=post_id)
    context = {
        'current_post': current_post,
    }
    return render(request, 'posts/post_detail.html', context)


def profile(request, username):
    user = get_object_or_404(User, username=username)
    username = user.username
    count_posts = user.posts.count()
    posts = user.posts.select_related('group')
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'username': username,
        'count_posts': count_posts,
        'page_obj': page_obj,
        }
    return render(request, 'posts/profile.html', context)


@login_required
def post_create(request):
    form = PostForm(
        request.POST or None)
    if form.is_valid():
        form.save(commit=False).author_id = request.user.pk
        form.save()
        return redirect('posts:profile', username=request.user)
    context = {
        'form': form,
        'groups': Group.objects.all()
    }
    return render(request, 'posts/post_create.html', context)


@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, id=post_id, author=request.user)
    form = PostForm(
        request.POST or None,
        instance=post)
    if request.user != post.author:
        return redirect('post:profile', username=request.user)
    if form.is_valid():
        form.save()
        return redirect('posts:post_detail', post_id)
    context = {
        'form': form,
        'post': post,
        'is_edit': True
    }
    return render(request, 'posts/post_create.html', context)
