"""
A context manager that adds the sql queries used to generate a page to the
request context.
"""

# copied straight out of http://www.djangosnippets.org/snippets/370/

from django.conf import settings
import django.db as db
from django.utils.html import escape
import re

# sql queries can be quite long and don't contain spaces in their select clause,
# which makes them unwrappable in html.
# from: http://www.djangosnippets.org/snippets/93/
enable_linebreaks_regex = re.compile(",(?! )")
def enable_linebreaks(str):
    return enable_linebreaks_regex.sub(",<wbr>", str)

# wraps around a query dict as provided by django, to output the sql part per 
# default if accessed without an index.
class SqlQuery(object):
    def __init__(self, query):
        self.query = query
    def __getitem__(self, k):
        return self.query[k]
    # per default, return the sql query
    def __str__(self):
        return enable_linebreaks(escape(self['sql']))

# provides sqldebug.queries
class SqlQueries(object):
    def __iter__(self):
        for q in db.connection.queries:
            yield SqlQuery(q)

    def __len__(self):
        return len(db.connection.queries)
    def count(self):
        return len(self)
    
    # per default, output as list of LI elements
    def __str__(self):        
        result = ""
        for q in self:
            result += "<li>" + escape(q["sql"]) + "</li>\n"
        return result            

# main class for sql debugging info
class SqlDebug(object):
    def __init__(self):
        # allow access to database queries via attribute
        self.queries = SqlQueries()
        
    # per default, display some basic information
    def __str__(self):
        return "%d queries, %f seconds" % (self.queries.count(), self.time())
        
    # checks whether sql debugging has been enabled
    def enabled(self):        
        return getattr(settings, 'SQL_DEBUG', False) and \
               getattr(settings, 'DEBUG', False)
    # shortcurt to enabled()
    def __nonzero__(self):
        return self.enabled()
        
    # returns aggregate time for db operations as a double
    def time(self):
        secs = 0.0
        for s in self.queries:
            secs += float(s['time'])
        return secs

# context processor function: makes a SqlDebug instance available to templates.
def sqldebug(request):
    return {'sqldebug': SqlDebug()}