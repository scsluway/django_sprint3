from django.utils import timezone
from django.shortcuts import render, get_object_or_404

from blog.models import Post, Category

NUMBER_OF_POSTS = 5


def filter_posts(manager=Post.objects):
    return manager.select_related(
        'category', 'author', 'location'
    ).filter(
        category__is_published=True,
        is_published=True,
        pub_date__lt=timezone.now()
    )


def index(request):
    return render(
        request,
        'blog/index.html',
        {'post_list': filter_posts()[:NUMBER_OF_POSTS]}
    )


def post_detail(request, post_id):
    post = get_object_or_404(filter_posts(), pk=post_id)
    return render(request, 'blog/detail.html', {'post': post})


def category_posts(request, category_slug):
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True
    )
    posts = filter_posts(category.posts)
    return render(
        request,
        'blog/category.html',
        {'category': category, 'post_list': posts}
    )
