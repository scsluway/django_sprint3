from datetime import datetime

from django.http import Http404
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, get_list_or_404

from blog.models import Post, Category


def index(request):
    posts = Post.objects.select_related(
        'category', 'author', 'location'
    ).filter(
        is_published=True,
        category__is_published=True,
        pub_date__lt=datetime.now()
    ).order_by('-id')[:5]
    return render(
        request, 'blog/index.html',
        {'post_list': posts})


def post_detail(request, post_id):
    post = get_object_or_404(
        Post.objects.select_related('category', 'author', 'location').filter(
            is_published=True,
            category__is_published=True,
            pub_date__lt=datetime.now()
        ), pk=post_id
    )
    return render(request, 'blog/detail.html', {'post': post})


def category_posts(request, category_slug):
    category = get_object_or_404(Category.objects.filter(slug=category_slug),
                                 is_published=True)
    posts = Post.objects.select_related('category').filter(
        is_published=True,
        category__slug=category_slug,
        pub_date__lt=datetime.now()
    ).order_by()
    return render(request, 'blog/category.html',
                  {'category': category, 'post_list': posts})
