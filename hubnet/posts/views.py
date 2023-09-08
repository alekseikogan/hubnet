from django.shortcuts import get_object_or_404, render

from .models import Group, Post


def index(request):
    posts = Post.objects.order_by('-pub_date')[:10]
    context = {
        'title': 'Последние обновления',
        'posts': posts,
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
