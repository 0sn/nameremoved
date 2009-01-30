#!/usr/bin/env python
# encoding: utf-8

import sys
import os
import urllib


from django.core.management import setup_environ
import settings
setup_environ(settings)

from comics.models import Comic

# WARNING
# This piece of crap hacky script hasn't been updated to the new version
# of the site and needs lots of changes and makes me sad.
# DO NOT RUN IT YET.

def main():
    # the transcription javascript that just HAPPENS to contain all the urls
    # I've submitted to the site. HOW HANDY IS THAT.
    f = urllib.urlopen("http://ohnorobot.com/js/48.js")
    urls = []
    for line in f:
        if "u[" in line and ']="s' in line:
            junk, number, morejunk = line.split('"')
            urls.append(int(number[1:]))
    urls.sort()
    last_ohnorobot = urls[-1]
    last_onsite = Comic.public_comics.count()

    api_url = "http://www.ohnorobot.com/api.pl?"

    for i in range(last_ohnorobot+1,last_onsite+1):
        which_comic = Comic.public_comics.all()[i-1]
        request = "&".join(["u=apyeU53//eqIY",
                            "p=peasy123",
                            "c=ADD",
                            "url=http://nameremoved.com/comics/%d/" % i,
                            "t=%s" % urllib.quote(which_comic.title),
                            "d=%s" % urllib.quote(which_comic.transcript)])
        rurl = urllib.urlopen(api_url+request)
        print which_comic.title
        for line in rurl:
            print line,
        print
    

if __name__ == '__main__':
    main()

