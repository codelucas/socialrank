from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('link.views',
    url('^about/$', 'about'),
    url('^refresh_links/$', 'refresh_links'),
    url('^$', 'home'),
    url('^.*/$', 'home'),
)