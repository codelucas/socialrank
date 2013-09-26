__author__ = 'Lucas Ou-Yang'

# -*- coding: utf-8 -*-

import json
from django.shortcuts import render_to_response, RequestContext
from django.http import HttpResponse, Http404

from link.models import Link
from socialrank.settings import get_root_url


LINK_DELIM = "&$$"


def render_with_context(request, template, cookies=[], kwargs={}):
    """our custom middleman render method, killing all
    the controller boilerplate. if we want code that is
    present in all responses like cookies, dump it here."""

    kwargs['root_url'] = get_root_url()

    response = render_to_response(template, kwargs,
        context_instance = RequestContext(request))

    for tup in cookies:
        response.set_cookie(tup[0], tup[1])

    return response


def refresh_links(request):
    """ajax post handler for the real time
    updating effect, we use json"""

    if request.method == 'POST':

        links = Link.objects.order_by('-hotness')[:50]
        ret_links = []

        for l in links:

            shares = str(l.shares)

            if not shares:
                shares = "0"

            if not l.url or not l.title or not l.status:
                continue

            img = l.img
            if not img:
                img = ""

            ret_links.append({'links':LINK_DELIM.join(
                [
                  l.url,
                  l.title,
                  img,
                  l.human_age(),
                  l.status,
                  shares
                ]
            )})

        ret_json = json.dumps({"data":ret_links})
        response = HttpResponse(ret_json,
                                mimetype="application/json")
        # response.set_cookie()
        return response

    else:
        raise Http404('What are you doing here?')


def home(request, template='home.html'):
    """/ root url of the site. it displays a listing
    of the top 100 news links which are in existence"""

    links = Link.objects.order_by('-hotness')[:50]

    return render_with_context(request, template=template,
                    kwargs={'links':links})


def about(request):
    return render_with_context(request, 'about.html')