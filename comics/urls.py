from django.conf.urls.defaults import *

from django.views.generic.list_detail import object_list
from models import Comic

urlpatterns = patterns('nr.comics.views',
    url(r'^$',
        object_list,
        {"queryset": Comic.comics.public(),"template_object_name":"comic"},
        name="archive"),
    url(r'^(?P<slug>\d+)/$', 'comic'),
    url(r'^(?P<slug>\d+)/image/$', 'comic_image'),
)
