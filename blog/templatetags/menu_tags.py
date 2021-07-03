from blog.models import Category, Post
from django import template

register = template.Library()


@register.inclusion_tag('include/tags/categories.html')
def get_categories(path):
    categories = Category.objects.all()
    posts = Post.objects.order_by('-id').prefetch_related('category')[:5]
    return {'list_category': categories, 'five_last_posts': posts, 'path': path}


@register.inclusion_tag('include/tags/sidebar_category.html')
def get_sidebar_categories():
    categories = Category.objects.all().prefetch_related('posts')
    return {'list_category': categories}


def get_value_by_key(dictionary, key_name):
    return dictionary.get(key_name, default=None)


register.filter('get_value_by_key', get_value_by_key)
