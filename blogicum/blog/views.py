from datetime import datetime

from django.shortcuts import render, get_object_or_404

from blog.models import Post, Category


def filter_posts(slug=None):
    posts = Post.objects.select_related(
        'category', 'author', 'location'
    ).filter(
        is_published=True,
        pub_date__lt=datetime.now()
    )
    return (posts.filter(category__is_published=True) if slug is None
            else posts.filter(category__slug=slug))


def index(request):
    return render(
        request, 'blog/index.html',
        {'post_list': filter_posts().order_by('-id')[:5]})


def post_detail(request, post_id):
    post = get_object_or_404(filter_posts(), pk=post_id)
    return render(request, 'blog/detail.html', {'post': post})


def category_posts(request, category_slug):
    category = get_object_or_404(Category,
                                 slug=category_slug,
                                 is_published=True)
    posts = filter_posts(category.slug)
    return render(request, 'blog/category.html',
                  {'category': category, 'post_list': posts})
