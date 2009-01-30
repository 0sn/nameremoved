from django.views import generic
from django.views.decorators.vary import vary_on_cookie
from models import Comic
from nr.utils import render_with_request
from django.http import HttpResponseRedirect, HttpResponsePermanentRedirect
import datetime
from django.shortcuts import get_object_or_404

COOKIE_AGE = 60 * 60 * 24 * 7 * 52

def with_cookie(response,which_comic):
    """sets the saved cookie on a response"""
    expires=datetime.datetime.strftime(datetime.datetime.utcnow() + 
               datetime.timedelta(seconds=COOKIE_AGE), 
                "%a, %d-%b-%Y %H:%M:%S GMT")
    response.set_cookie(
        "saved_comic",
        which_comic,
        max_age = COOKIE_AGE,
        expires = expires,
        path = "/",
    )
    return response

@vary_on_cookie
def index(request):
    """the front page"""
    comic = Comic.comics.public().order_by('-date')[0]
    
    new_visitor = "saved_comic" not in request.COOKIES
    try: saved_id = int(request.COOKIES["saved_comic"])
    except (ValueError, KeyError): saved_id = comic.sequence
    
    # the guide is only shown if you missed a comic or were browsing the archives
    showguide = (comic.sequence - saved_id) > 1
    
    response = render_with_request(
        "comics/front.html",
        {"comic": comic, "saved": Comic.comics.get(sequence=saved_id), "showguide": showguide, "new_visitor": new_visitor},
        request
    )
    return with_cookie(response, comic.sequence)

def comic(request, slug):
    """the page of an individual comic"""
    comic = get_object_or_404(Comic, sequence=slug)
    response = render_with_request(
        "comics/comic_detail.html",
        {"comic": comic},
        request
    )
    return with_cookie(response, comic.sequence)

def comic_image(request, slug):
    """the image for a particular comic"""
    c = get_object_or_404(Comic, sequence=int(slug))
    return HttpResponsePermanentRedirect(c.comic.url)
