from django.contrib.sitemaps import FlatPageSitemap, GenericSitemap, Sitemap
from nr_comics.models import Comic
import datetime

def last_today(instance, item):
    return datetime.date.today()

static_pages = [
    {'name':'Front Page', 'priority': 1.0, 'location': '/', 'freq': 'daily'},
    {'name':'Archive', 'priority': 0.5, 'location': '/comics/', 'freq': 'weekly'},
    {'name':'Contributions', 'priority': 0.6, 'location': '/contribute/', 'freq': 'weekly'}
]

class StaticSitemap(Sitemap):
    def changefreq(self, item):
        return item['freq']
    
    def location(self, item):
        return item['location']
    
    def lastmod(self, item):
        return datetime.date.today()
    
    def priority(self, item):
        return item['priority']
    
    def items(self):
        return static_pages

sitemap = {
    'comics': GenericSitemap({
        'queryset': Comic.comics.public(),
        'date_field': 'date',
        'priority': 0.8,
        'changefreq': 'monthly',
    }),
    'flatpages': FlatPageSitemap,
    'static': StaticSitemap,
}

