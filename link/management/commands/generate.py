"""
    NOTE: There is something critical which is
    broken and i don't have time to fix during this
    hackathon. For some reason my appengine crontab
    timers are not working as expected (i'm getting 301
    redirects), so a weird hack which worked was just adding
    a generate_links() call at the bottom of this file
    versus praying calling the function from urls.py
    will work.

    I also do this in link/update.py

"""

__author__ = 'Lucas Ou-Yang'

import feedparser
import requests
from time import time
from datetime import datetime
import MySQLdb as Database
from warnings import filterwarnings
from cookielib import CookieJar as cj
from dateutil.parser import parse as dateparse
from django.core.management.base import BaseCommand

from lib.web import urlopen, fb_shares, top_image
from lib.sources import feeds
from link.models import Link

request_kwargs = {
    'headers' : {
        'User-Agent': 'Mozilla/5.0 (compatible; MSIE 9.0; '
            'AOL 9.7; AOLBuild 4343.19; Windows NT 6.1; '
            'WOW64; Trident/5.0; FunWebProducts)'
    },
    'cookies' : cj(),
    'timeout' : 10
}

class Command(BaseCommand):

    def handle(self, *args, **options):
        """extracts content from sources and generates
        links, would add multi-threading but ran out of time"""

        filterwarnings('ignore', category=Database.Warning)
        s1 = time()

        for f in feeds:
            generate_links(f)

        gen_reddit_links() # custom method for reddit

        print 'scraped all feeds in %s minutes' % \
                ((time() - s1)/60)


def generate_links(feed):
    """parsing out news articles from a pre-provided
    list of feeds from our other scraper. The most
    important thing in this function is to note that
    all our datetime objects are stripped of their timezones.

    News feeds default set all of their publishing times to UTC,
    so our backend math all operates on UTC

    We will cache all of the urls to a txt file to reduce
    re-crawling identical urls -- 10 minutes"""

    dom = feedparser.parse(feed)

    if not dom.get('entries'):
        print 'feedparser unable to parse'
        return []

    entries = dom['entries']

    _entries = []

    for e in entries:
        if e.get('published'):
            try:
                dateparse(e['published'])
            except AttributeError:
                print 'publish fail on %s' % feed
                continue
            _entries.append(e)

    extract = [

        (e['link'], e['title'], dateparse(e['published']).
                                    replace(tzinfo=None))

            for e in _entries if e.get('link') and e.get('title')
    ]

    tot = 0

    for e in extract:

        try:
            shares = fb_shares(e[0])

        except Exception, e:
            print 'fb shares fail on link: ' \
                  '%s for %s' % (e[0], str(e))
            continue

        if not shares:
            continue

        try:
            html = urlopen(e[0])

        except Exception, e:
            print str(e)
            # try:
            #    l = Link(url=e[0], title=e[1], birth=e[2],
            #                           shares=shares)
            continue
            # except:
            #    continue # there isn't enough time :,(

        # if the html download works, extract top img and
        # proceed to save the link
        else:
            try:
                link_img = top_image(html)
                l = Link(url=e[0], title=e[1], birth=e[2],
                            img=link_img, shares=shares)
                l.save()
                tot += 1

            except:
                continue

        # try:
        #    l.save()
        # except Exception, e:
        #    This will error if we re-scrape an
        #    already existing link
        #    print str(e)
        #    continue

    print 'we saved %d total links from %s' % (tot, feed)


def unix_to_datetime(unix):
    """reddit serves unix timestamps, this
    method converts unix time into python
    datetime objects"""

    try:
        unix = int(float(unix))
        str_time = datetime.fromtimestamp(unix).\
            strftime('%Y-%m-%d %H:%M:%S')
        dt = dateparse(str_time)

    except Exception, e:
        print str(e)
        return None

    return dt



def gen_reddit_links():
    """so much hardcoding, this was done because of
    time constraints."""

    reddit_anchors = [
        'http://www.reddit.com/',
        'http://www.reddit.com/r/pics/',
        'http://www.reddit.com/r/funny/',
        'http://www.reddit.com/r/gaming/',
        'http://www.reddit.com/r/worldnews/',
        'http://www.reddit.com/r/news/',
        'http://www.reddit.com/r/technology/',
        'http://www.reddit.com/r/science/'
    ]

    reddit_anchors = [ r+'.json' for r in reddit_anchors ]

    saved = 0

    for r in reddit_anchors:

        try:
            dat = requests.get(r, **request_kwargs).json()

        except Exception, e:
            print str(e)
            continue

        links = []
        if dat.get('data') and dat['data'].get('children'):
            links = dat['data']['children']

        links = [

            (
                l['data']['url'],
                l['data']['title'],
                l['data'].get('thumbnail'),
                unix_to_datetime(l['data']['created'])
            )

            for l in links
                if l.get('data') and
                    l['data'].get('title') and
                    l['data'].get('url') and
                    l['data'].get('created')
        ]

        links = [ l for l in links if l[3] ]

        for l in links:

            try:
                shares = fb_shares(l[0])

            except Exception, e:
                print 'fb fail on reddit link: ' \
                      '%s for %s' % (l[0], str(e))
                continue

            if not shares:
                continue

            try:
                l = Link(url=l[0], title=l[1], birth=l[3],
                            img=l[2], shares=shares)
                l.save()
                saved += 1

            except Exception, e:
                print str(e)
                continue


    print 'we saved %d total links from reddit' % saved

