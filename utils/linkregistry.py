"""
Flatpages don't have any other home, being a django.contrib app. So they
are added to the flatpage registry right here.
"""
from nr.utils.context.navigation import linkregistry
from django.core.cache import cache

CACHE_TIME = 60 * 10

def flatpage_root():
    """
    This function creates the list of root flatpages, not including "/".
    """
    cache_key = "flatpage_linkregistry_list"
    c = cache.get(cache_key)
    if c is None:
        from django.db import models
        pages = []
        model = models.get_model("flatpages", "FlatPage")
        if model:
            for page in model.objects.filter(url__regex=r'^/[^/]*/$'):
                pages.append((page.url,page.title))
        c = pages
        cache.set(cache_key,c,CACHE_TIME)
    return c

linkregistry.register_dynamic(flatpage_root)
