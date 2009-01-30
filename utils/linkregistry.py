"""
Flatpages don't have any other home, being a django.contrib app. So they
are added to the flatpage registry right here.
"""
from nr.utils.context.navigation import linkregistry

def flatpage_root():
    """
    This function creates the list of root flatpages, not including "/".
    """
    from django.db import models
    pages = []
    model = models.get_model("flatpages", "FlatPage")
    if model:
        for page in model.objects.filter(url__regex=r'^/[^/]*/$'):
            pages.append((page.url,page.title))
    return pages

linkregistry.register_dynamic(flatpage_root)
