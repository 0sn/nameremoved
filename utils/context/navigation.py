"""
The root menu generator for the site.

In your app, make a file "linkregistry.py", import the linkregistry instance
defined below, and call either::

    linkregistry.register_dynamic()
    
or::

    linkregsitry.register_static()

to add links to the main navigation menu.

The function nav at the bottom is the context manager which adds the generated
menu to the request context for use in templates.

Put it in TEMPLATE_CONTEXT_PROCESSORS

Also you should add the autodiscover function to your main urls, like with
the admin autodiscover.
"""

class AlreadyRegistered(Exception):
    pass


class LinkRegistry(object):
    """
    Stores the root links across the entire site. Use it by importing
    "linkregistry" from this module and calling either::
    
    linkregistry.register_dynamic()
    
    or::
    
    linkregistry.register_static()
    """
    def __init__(self):
        self.static = []
        self.dynamic = []
    
    def register_static(self, url, title):
        """
        Registers the given url with the given title.
        Both are strings::
        
            linkregistry.register_static("/", "Home")
            linkregistry.register_static("/comics/", "Archive")
        """
        if url in (x[0] for x in self.static):
            raise AlreadyRegistered("The url %s is already registered.") % url
        self.static.append((url,title))
    
    def register_dynamic(self, mapping):
        """
        Registers a callable that generates a set of urls on demand.
        The callable should take no arguments and return a list of tuples in
        (url,title) format::
        
            linkregistry.register_dynamic(some_function)
        
        See flatpage_root in this module for an example.
        """
        if callable(mapping):
            self.dynamic.append(mapping)
        else:
            raise TypeError("The argument should be a callable.")


linkregistry = LinkRegistry()
    

def autodiscover():
    # stolen from django.contrib.admin.__init__
    # does the autodiscovery of linkregistry modules
    import imp
    from django.conf import settings

    for app in settings.INSTALLED_APPS:
        try:
            app_path = __import__(app, {}, {}, [app.split('.')[-1]]).__path__
        except AttributeError:
            continue

        try:
            imp.find_module('linkregistry', app_path)
        except ImportError:
            continue

        __import__("%s.linkregistry" % app)

def nav(request):
    """
    Adds a useful name into the current context: root_pages ...
    It's the "top-level" flatpages.
    First the static urls from the link registry are added, then the
    dynamic ones. Sorry, flatpages, but you're coming in last!
    """
    root = []
    root += linkregistry.static
    for url_set in linkregistry.dynamic:
        root += url_set()
    return {"root_pages":root}
