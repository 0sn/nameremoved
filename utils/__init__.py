"""
Extra functions and utilites are in this app.

utils.render_with_request returns an HttpResponse with a RequestContext

utils.context.navigation and utils.context.sqldebug are two handy context
managers, the former for managing the site-wide navigation and the latter
for seeing the current sql commands in DEBUG mode.

utils.management.commands.bonjour adds a new way to run the debug server,
advertising it over the bonjour network.

utils.templatetags.flatpage contains a handy template tag for dropping a
hierarchy of flatpages into the flatpage template (for building menus)
"""

from django.shortcuts import render_to_response
from django.template import RequestContext

def render_with_request(template, context, request):
    """
    Returns an HttpResponse just like render_to_response except with the
    current request added to the context.
    """
    return render_to_response(
        template,
        context,
        context_instance=RequestContext(request)
    )

# but see for an interesting alternative
# http://lincolnloop.com/blog/2008/may/10/getting-requestcontext-your-templates/

