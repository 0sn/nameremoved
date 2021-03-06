from django.conf.urls.defaults import *
from django.conf import settings
from django.http import HttpResponsePermanentRedirect, HttpResponseGone, HttpResponse
from nr_comics.feeds import LatestEntries
from sitemap import sitemap

from django.contrib import admin
admin.autodiscover()

from nr_linkmanager.context import navigation
navigation.linkregistry.register_static("/","Home")
navigation.linkregistry.register_static("/comics/", "Archive")
navigation.linkregistry.register_static("/storylines/", "Storylines")
navigation.linkregistry.register_static("/contribute/", "Contribute")
navigation.autodiscover()


def old_feed(request):
    """People should use the feedburner url for their feeds."""
    return HttpResponsePermanentRedirect("http://feeds.feedburner.com/NameRemoved")

urlpatterns = patterns('',
    (r'^$', 'nr_comics.views.index'),
    
    (r'^comics/', include('nr_comics.urls')),
    (r'^contribute/', include('nr_contributions.urls')),
    
    (r'^storylines/', include('nr_storylines.urls')),
    
    (r'^feeds/latest/$', old_feed),
    (r'^feeds/(?P<url>.*)/$',
         'django.contrib.syndication.views.feed',
         {'feed_dict': {'feedburner': LatestEntries}}),
    
    (r'^sitemap.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemap}),
    
    (r'^admin/nr_contributions/report/$', 'nr_contributions.views.report'),
    (r'^admin/memcache/$', 'nr_utils.mstat.view'),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/(.*)', admin.site.root),
)

# redirects for old urls

def no_extra(request, rest_of_path):
    """used to have 'extra' objects instead of flatpages!"""
    return HttpResponsePermanentRedirect(rest_of_path)

def old_index(request):
    """sends everyone with the old bad php comic app url to the front page"""
    return HttpResponsePermanentRedirect("/")

def favicon(request):
    """the favicon lives on the static server"""
    return HttpResponsePermanentRedirect("http://static.nameremoved.com/favicon.ico")

def movedpics(request, rest_of_path):
   """the old pics directory lives on the static server"""
   return HttpResponsePermanentRedirect("http://static.nameremoved.com/pix" + rest_of_path)

def randomimage(request):
    """the random images aren't around any more"""
    return HttpResponseGone()

def robots(request):
    """Don't try adding a closing / to the robots.txt request."""
    return HttpResponse("")

urlpatterns += patterns('',
    (r'^extra(/.*)', no_extra),
    (r'^feed/rss.xml$', old_feed),
    (r'^index.php', old_index),
    (r'^favicon\.ico', favicon),
    (r'^pix(/.*)', movedpics),
    (r'^randomimage/.*', randomimage),
    (r'^robots.txt$', robots),
)

# static serving for debug mode

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT }),
        (r'^comic_files/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT + 'comic_files'}),
    )
