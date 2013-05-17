'''
Created on 2012-7-25

@author: TheBeet
'''
from django.conf.urls.defaults import patterns, url, include

from views import ContestDetailView, ContestListView, ContestStatisticView, ContestProblemView, ContestRankView

urlpatterns = patterns('',
    url(r'^(?P<pk>\d+)/$', ContestDetailView.as_view(), name="detail"),
    url(r'^(?P<pk>\d+)/statistic/$', ContestStatisticView.as_view(), name="statistic"),
    url(r'^(?P<pk>\d+)/problem/(?P<problem>\w)/$', ContestProblemView.as_view(), name="problem"),
    url(r'^now/$', ContestListView.as_view(), name="list", kwargs={"status":"now"}),
    url(r'^past/$', ContestListView.as_view(), name="list", kwargs={"status":"past"}),
    url(r'^scheduled/$', ContestListView.as_view(), name="list", kwargs={"status":"scheduled"}),
    url(r'^$', ContestListView.as_view(), name="list"),
    url(r'^(?P<contest_id>\d+)/rank', ContestRankView.as_view(), name="rank"),
)

