__author__ = 'Lucas Ou-Yang'

from django.db import models
from django.utils import timezone
from datetime import datetime

# -*- coding: utf-8 -*-

class Link(models.Model):
    """
    abstraction of a web link

    likes are the # of facebook shares that
    any particular url has.
    located @: http://graph.facebook.com/{{ url }}

    birth is the publication date of the url.
    if we fail at extracting it, we just set it to
    the extraction date of that url.

    rank is an integer indicating the previous
    rank of the link. we are storing this because
    we will show an up or down arrow depending if
    the link drops or goes up in rank.

    """

    url = models.URLField(unique=True)
    title = models.CharField(max_length=200)
    birth = models.DateTimeField(default=timezone.now)
    shares = models.IntegerField(default=0)
    img = models.URLField(blank=True, null=True)
    rank = models.IntegerField(blank=True, null=True)
    status = models.CharField(max_length=50, default='EQUAL')
    hotness = models.IntegerField(default=0)


    def save(self, *args, **kwargs):
        """if it's needed to override some settings
        pre-save, just add that code in here before
        the 'super' initializer"""

        super(Link, self).save(*args, **kwargs)
        self.set_hotness()


    def set_hotness(self):
        """due to the nature of news, we value age
        an order of magnitude greater than shares"""

        self.hotness = (self.shares /
                    (self.raw_age()*1.1))*100000


    def raw_age(self):
        """takes a datetime and returns
        the raw age in seconds"""

        epoch = datetime(1970, 1, 1, 0, 0, 0, 0)

        age = datetime.now() - self.birth

        seconds = age.days*86400 + age.seconds \
                + (float(age.microseconds) / 1000000)

        return seconds


    def human_age(self):
        """Returns a humanized string representing time difference
        between now() and the input timestamp.

        The output rounds up to days, hours, minutes, or seconds.
        4 days 5 hours returns '4 days'
        0 days 4 hours 3 minutes returns '4 hours', etc..."""

        diff = datetime.now() - self.birth

        days = diff.days
        hours = diff.seconds/3600
        minutes = diff.seconds%3600/60
        seconds = diff.seconds%3600%60

        str_ = ""
        tstr = ""

        if days > 0:
            if days == 1:   tstr = "day"
            else:           tstr = "days"
            str_ = str_ + "%s %s" % (days, tstr)
            return str_

        elif hours > 0:
            if hours == 1:  tstr = "hour"
            else:           tstr = "hours"
            str_ = str_ + "%s %s" % (hours, tstr)
            return str_

        elif minutes > 0:
            if minutes == 1:tstr = "min"
            else:           tstr = "mins"
            str_ = str_ + "%s %s" % (minutes, tstr)
            return str_

        elif seconds > 0:
            if seconds == 1:tstr = "sec"
            else:           tstr = "secs"
            str_ = str_ + "%s %s" % (seconds, tstr)
            return str_

        else:
            return ""