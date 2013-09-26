"""
    This is terrible terrible code, never replicate.

    If google appengine was easier to configure and
    django-nonrel (not django) was more user friendly
    then maybe something cooler would be been
    produced.

"""

__author__ = 'Lucas Ou-Yang'

from link.models import Link
from lib.web import fb_shares

from django.core.management.base import BaseCommand
from warnings import filterwarnings
import MySQLdb as Database
import gc

# Limit top 500 news pieces for this hackathon
# this will be scaled up after!
MAX_LINKS = 500

class Command(BaseCommand):

    def handle(self, *args, **options):
        """does not just update the shares/hotness but
        it also only keeps top 1K urls and purges the rest

        on a timer, 1K calls to Facebook's graph api will take
        roughly ONE MINUTE"""

        filterwarnings('ignore', category=Database.Warning)

        links = queryset_iterator(Link.objects.all())

        for l in links:

            try:
                shares = fb_shares(l.url)

            except Exception, e:
                print 'fb fail on %s because %s' % (l.url, str(e))
                # l.delete()
                continue

            if shares is None:
                print 'shares error, received None but ' \
                      'old shares was %s' % l.shares
                # l.delete()
                continue

            # TODO prev = l.shares
            # TODO l.slope = l.shares - prev

            l.shares = shares
            l.save()

        links_ = Link.objects.order_by('-hotness')

        good_links = links_[:MAX_LINKS]
        bad_links = links_[MAX_LINKS:]

        for b in bad_links:
            b.delete()

        # tag each link with a status, so we can display
        # fancy UI to the users. Tag a new rank. We have
        # a cool setup so new articles are treated with no rank

        # a not so risky hack that if two articles have the same like
        # count and are no zero they are duplicates.
        # I'm running out of time and don't wanna implement a fuzzy
        # title comparison or canonical url search

        uniq = {}

        for new_rank, l in enumerate(good_links):

            if l.shares != 0 and uniq.get(l.shares):
                l.delete()
                continue
            else:
                uniq[l.shares] = l

            if l.rank:
                if new_rank < l.rank:
                    l.status = 'POSITIVE'
                elif new_rank > l.rank:
                    l.status = 'NEGATIVE'
                else:
                    l.status = 'EQUAL'
            else:
                l.status = 'EQUAL'

            l.rank = new_rank
            l.set_hotness()
            l.save()

        print 'updating finished!'


def queryset_iterator(queryset, chunksize=1000):
    """Iterate over a Django Queryset ordered by the primary key

    This method loads a maximum of chunksize (default: 1000) rows in it's
    memory at the same time while django normally would load all rows in it's
    memory. Using the iterator() method only causes it to not preload all the
    classes.

    Note that the implementation of the iterator does not support ordered
    query sets."""

    pk = 0
    last_pk = queryset.order_by('-pk')[0].pk
    queryset = queryset.order_by('pk')
    while pk < last_pk:
        for row in queryset.filter(pk__gt=pk)[:chunksize]:
            pk = row.pk
            yield row
        gc.collect()