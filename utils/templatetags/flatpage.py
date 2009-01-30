from django import template
import re
from django.contrib.flatpages.models import FlatPage
register = template.Library()

def do_flatpage_children(parser, token):
    """
    This tag creates a queryset containing all flatpages below a given root
    url, adding it to the current context with the name "flatpage_children".
    It also adds the flatpage of the root url to the context with the name
    flatpage_root.
    
    A "root url" is any url matched by ^/[^/]*/$.
    
    Typically, this would be used to get a list of children of a parent url::
    
        {% flatpage_children "/about/"}
    
    This adds a queryset of all deeper urls, such as "/about/author/" and
    "/about/pants/" to the current context, named flatpage_children. It also
    adds the flatpage named by "/about/" to the current context, named
    flatpage_root.
    
    If the url given is "/", the tag doesn't do anything.
    
    If the url given is not a root url, for example "/about/pants/", only the
    root url portion of the argument is used. Thus, "/about/" and
    "/about/pants/" will return the same result, assuming both those flatpages
    exist.
    
    If the first argument is not in quotes, it is assumed to be in the current
    context::

        {% flatpage_children flatpage.url %}
    
    This adds a queryset of all urls deeper than the root url of the current
    flatpage. And the root flatpage to boot.
    """
    bits = token.contents.split()
    if len(bits) != 2:
        raise template.TemplateSyntaxError("%r expected format is 'flatpage_children URL_or_name'" % bits[0])
    return FlatpageChildren(bits[1])

class FlatpageChildren(template.Node):
    # this regex is the definition of a top-level flatpage
    # override in a subclass if you have a different idea!
    root_regex = r'^(/[^/]*?/)'
    def __init__(self, url):
        self.url = url
    def render(self, context):
        if self.url[0] in ('"',"'"):
            if self.url[0] == self.url[-1] and len(self.url) > 3:
                urlcontent = self.url
            else:
                return ""
        else:
            urlcontent = template.Variable(self.url).resolve(context)
        m = re.search(self.root_regex, urlcontent)
        if not m:
            return ""
        root = m.group(1)
                
        context["flatpage_children"] = FlatPage.objects.filter(
            url__gt=root,
            url__startswith=root
        ).order_by('title')
        context["flatpage_root"] = FlatPage.objects.get(url=root)
        return ""

register.tag('flatpage_children', do_flatpage_children)

# from http://www.djangosnippets.org/snippets/654/

from django.conf import settings
from django.template.defaultfilters import stringfilter

@register.filter
@stringfilter
def media_url(value):
    """Searches for {{ MEDIA_URL }} and replaces it with the MEDIA_URL from settings.py"""
    return value.replace('{{ MEDIA_URL }}', settings.MEDIA_URL)
media_url.is_safe = True
