socialrank
==========

Visit the site [here](http://socialrank.codelucas.com). I also have a [blog](http://codelucas.com).

My submission for the Pennapps 2013 hackathon. SocialRank is a content & meme aggregator 
which combines Facebook's social media with Reddit's famous hotness algorithm. 
The content also updates in real time. 

Check out my other project, [`Wintria`](http://wintria.com), if you'd to see a news search engine which i'm working on at the moment as a startup. 

**NOTE**: If you'd actually try to deploy this there are two things which must be added.

First is your own settings.py and be sure to
include values for:

```get_root_url()```

```FB_APP_ID```

```FB_APP_SECRET```

You also need to set up a crontab assuming you are on a linux server setup. This is
because socialrank's crawlers need to be pulling news from other websites on a timed
interval. 

Here are crontab [examples](http://www.thegeekstuff.com/2009/06/15-practical-crontab-examples/)

If you want to deploy this app and you are having trouble please contact me!


