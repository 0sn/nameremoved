from django.contrib.syndication.feeds import Feed
from models import Comic
import datetime

class LatestEntries(Feed):
    title = "NAME REMOVED the webcomic"
    link = "http://nameremoved.com/"
    description = "A regular feed of irregular comics."
    author_name = "Nicholas Wolfe"
    copyright = "Copyright (c) 2008, Nicholas Wolfe. All rights reserved."
    
    def items(self):
        return Comic.comics.public().order_by('-date')[:10]
    
    def item_pubdate(self, item):
        """
        The date the comic was published. In Django 1.0 item_pubdate is
        expected to be a python datetime object, so I make one with a dummy
        time component.
        """
        return datetime.datetime.combine(item.date,datetime.time(0,0,0,0))