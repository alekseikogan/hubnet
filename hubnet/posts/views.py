from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from .models import Group, Post, User


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
