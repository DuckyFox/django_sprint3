from django.shortcuts import get_object_or_404, render
from django.db.models import Q
from blog.models import Post
from datetime import datetime as dt


def index(request):
    template = 'blog/index.html'
    post = get_object_or_404(
        Post.objects.values(
            'pub_date', 'is_published',
            'location', 'location__is_published',
            'category__title', 'title'
        ).filter(
            Q(is_published=True)
            & Q(category__is_published=True)
            & Q(pub_date__lte=dt.now())
        ).order_by('pub_date')[0:5],
        is_published=False
    )
    context = {'post': post}
    return render(request, template, context)


def post_detail(request):
    post = get_object_or_404(
        Post.objects.values(
            'pub_date', 'is_published',
            'location', 'location__is_published',
            'category__title', 'title', 'location__name'
        ).filter(
            Q(is_published=True)
            & Q(category__is_published=True)
            & Q(pub_date__lte=dt.now())
        ).order_by('pub_date')[0:5],
        (Q(is_published=False)
         | Q(pub_date__gte=dt.now())
         | Q(category__is_published=False))
    )
    template = 'blog/detail.html'
    context = {'post': post}
    return render(request, template, context)


def category_posts(request):
    template = 'blog/category.html'
    category = get_object_or_404(
        Post.objects.values(
            'category__description',
            'category__title',
            'category__slug__is_published',
        ).filter(
            Q(is_published=True)
            & Q(category__is_published=True)
            & Q(pub_date__lte=dt.now())
        ).order_by('pub_date')[0:5],
        category__is_published=False
    )
    context = {'category': category}
    return render(request, template, context)
