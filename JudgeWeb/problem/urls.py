'''
Created on 2012-7-25

@author: TheBeet
'''
from django.conf.urls.defaults import patterns, url

from views import ProblemDetailView, ProblemListView, ProblemStatisticView, ProblemVolumeView, ProblemSearchView, ajax_fav, ProblemFavListView

urlpatterns = patterns('',
    url(r'^fav/$', ajax_fav, name="fav"),
    url(r'^favproblem/$', ProblemFavListView.as_view(), name="favproblem"),
    url(r'^(?P<pk>\d+)/$', ProblemDetailView.as_view(), name="detail"),
    url(r'^statistic/(?P<pk>\d+)/$', ProblemStatisticView.as_view(), name="statistic"),
    url(r'^$', ProblemListView.as_view(), name="list"),
    url(r'^order/solve/$', ProblemListView.as_view(), name="order", kwargs={"order": "solve"}),
    url(r'^volume/(?P<volume>\d+)/$', ProblemVolumeView.as_view(), name="volume"),
    url(r'^volume/$', ProblemVolumeView.as_view(), name="volume"),
)
