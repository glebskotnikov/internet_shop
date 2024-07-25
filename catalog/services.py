from django.conf import settings
from django.core.cache import cache
from django.db.models import QuerySet

from catalog.models import Product, Category


def get_cached_categories():
    """Получает данные по категориям из кэша, если кэш пуст, получает данные из бд"""
    if settings.CACHE_ENABLED:
        key = 'categories_list'
        categories_list = cache.get(key)
        if categories_list is None:
            categories_list = Category.objects.all()
            cache.set(key, categories_list)
    else:
        categories_list = Category.objects.all()
    return categories_list


def get_cached_products(is_published: bool) -> QuerySet:
    """Получает данные по продуктам из кэша, которые опубликованы, если кэш пуст, то получает данные из бд"""
    key = 'published_products' if is_published else 'all_products'
    products = cache.get(key)
    if products is None:
        products = Product.objects.filter(is_published=is_published) if is_published else Product.objects.all()
        if settings.CACHE_ENABLED:
            cache.set(key, products)
    return products
