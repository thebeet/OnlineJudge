'''
Created on 2012-9-1

@author: Macro
'''
from django.conf.urls.defaults import patterns, url

from views import DiscussListView, DiscussDetailView

urlpatterns = patterns('',
    url(r'^$', DiscussListView.as_view(), name="list"),
    url(r'^problem/(?P<problem>\d+)/$', DiscussListView.as_view(), name="list"),
    url(r'^(?P<pk>\d+)/$', DiscussDetailView.as_view(), name="detail"),
)