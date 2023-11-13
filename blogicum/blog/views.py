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


def post_detail(request, id):

    post = get_object_or_404(
    Post.objects.all().filter(
             Q(is_published=True)
             & Q(category__is_published=True)
             & Q(pub_date__lte=dt.now())
         ),
         (Q(is_published=True)
          | Q(pub_date__gte=dt.now())
          | Q(category__is_published=False)) & (Q(id=id))
     )
    # Остальная часть вашего представления (view) остается без изменений
    template = 'blog/detail.html'
    context = {'post': post}
    return render(request, template, context)


def category_posts(request, category_slug):
    template = 'blog/category.html'

    posts = Post.objects.filter(
        Q(is_published=True)
        & Q(category__is_published=True)
        & Q(pub_date__lte=dt.now())
        & Q(category__slug=category_slug)
    ).order_by('pub_date')[0:10]

    category = get_object_or_404(Category, slug=category_slug, is_published=True)

    context = {'category': category, 'post_list': posts}
    return render(request, template, context)
