Socialrank
==========

http://socialrank.codelucas.com - website 

http://wintria.com   - startup

http://codelucas.com - personal blog


My submission for the Pennapps 2013 hackathon. SocialRank is a content & meme aggregator which combines Facebook's social media with Reddit's famous hotness algorithm. The content updates in real time. 

The scraper in this project was subpar because we had 1.5 days of time for the contest and the point of socialrank was not about the volume of news generated but how the content is organized. Check out my other project, Wintria, if you'd to see a news search engine which i'm working on at the moment as a startup. The scraper in Wintria is much stronger than socialrank and even other large aggregators today.

NOTE: If you'd actually try to deploy this there are two things which must be added.
This is a django application, I hid all of this application's sensitive information in
the settings.py, which was removed from this respository. 

Create your own settings.py and be sure to
include values for:

get_root_url()

FB_APP_I

FB_APP_SECRET

You also need to set up a crontab assuming you are on a linux server setup. This is
because socialrank's crawlers need to be pulling news from other websites on a timed
interval. 

Here are crontab examples: http://www.thegeekstuff.com/2009/06/15-practical-crontab-examples/

If you want to deploy this app and you are having trouble please contact me!


