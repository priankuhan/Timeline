from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('timeline.views',
    (r'^doc/(?P<id>\w+)/','detail'),
    (r'^$','index'),
    (r'^(?P<type>\w+)/','index'),
)

