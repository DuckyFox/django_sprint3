from django.shortcuts import get_object_or_404, render
from django.db.models import Q
from blog.models import Post
from blog.models import Category
from blog.models import Location
from datetime import datetime as dt


def index(request):
    template = 'blog/index.html'
    post_list = Post.objects.all().filter(
        Q(is_published=True)
        & Q(category__is_published=True)
        & Q(pub_date__lte=dt.now())
    ).order_by('pub_date')[0:5]
    context = {'post_list': post_list}
    return render(request, template, context)


def post_detail(request, pk):
    post = get_object_or_404(
        Post.objects.all().filter(
            Q(is_published=True)
            & Q(category__is_published=True)
            & Q(pub_date__lte=dt.now())
        ),
        (Q(is_published=False)
         | Q(pub_date__gte=dt.now())
         | Q(category__is_published=False)) & (Q(pk=pk))
    )
    # Остальная часть вашего представления (view) остается без изменений
    template = 'blog/detail.html'
    context = {'post': post}
    return render(request, template, context)


def category_posts(request):
    template = 'blog/category.html'
    category = get_object_or_404(
        Post.objects.all().filter(
            Q(is_published=True)
            & Q(category__is_published=True)
            & Q(pub_date__lte=dt.now())
        ).order_by('pub_date')[0:5],
        category__is_published=False
    )
    context = {'category': category}
    return render(request, template, context)
