from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.cache import cache_page

from hubnet.posts.utils import paginator_context

from .forms import CommentForm, PostForm
from .models import Follow, Group, Post, User


@cache_page(20)
def index(request):
    page_obj = paginator_context(
        Post.objects.order_by('-pub_date'),
        request)
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
    form = CommentForm()
    comments = current_post.comments.select_related('post')
    context = {
        'current_post': current_post,
        'form': form,
        'comments': comments
    }
    return render(request, 'posts/post_detail.html', context)


def profile(request, username):
    user = get_object_or_404(User, username=username)
    username = user.username
    count_posts = user.posts.count()
    page_obj = paginator_context(
        user.posts.select_related('group'),
        request)
    context = {
        'username': username,
        'count_posts': count_posts,
        'page_obj': page_obj,
        }
    return render(request, 'posts/profile.html', context)


@login_required
def post_create(request):
    form = PostForm(
        request.POST or None,
        files=request.FILES or None)
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
        files=request.FILES or None,
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


@login_required
def add_comment(request, post_id):
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = get_object_or_404(Post, id=post_id)
        comment.save()
    return redirect('posts:post_detail', post_id=post_id)


@login_required
def follow_index(request):
    posts = Post.objects.filter(
        author__in=request.user.follower.values_list('author')
    )
    page_obj = paginator_context(
        posts,
        request
    )
    context = {
        'posts': posts,
        'page_obj': page_obj,
        }
    return render(request, 'posts/follow_index.html', context)


@login_required
def profile_follow(request, username):
    author = get_object_or_404(User, username=username)
    if request.user != author:
        Follow.objects.get_or_create(
            user=request.user,
            author=author
        )
    return redirect('posts:profile', username=username)


@login_required
def profile_unfollow(request, username):
    Follow.objects.filter(
        user=request.user,
        author=User.objects.get(username=username)
    ).delete()
    return redirect('posts:profile', username=username)