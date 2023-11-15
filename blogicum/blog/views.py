from datetime import datetime as dt

from django.shortcuts import get_object_or_404, render
from django.db.models import Q

from blog.models import Post
from blog.models import Category


def suitable_posts():
    return Post.objects.select_related('category', 'location', 'author').filter(
        is_published=True,
        category__is_published=True,
        pub_date__lte=dt.now()
    )


def index(request):
    template = 'blog/index.html'
    post_list = suitable_posts()[:5]
    context = {'post_list': post_list}
    return render(request, template, context)


def post_detail(request, post_id):
    post = get_object_or_404(
        suitable_posts(),
        id=post_id
    )
    template = 'blog/detail.html'
    context = {'post': post}
    return render(request, template, context)


def category_posts(request, category_slug):
    template = 'blog/category.html'
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True)
    posts = suitable_posts().filter(
        category=category
    )
    context = {'category': category, 'post_list': posts}
    return render(request, template, context)
