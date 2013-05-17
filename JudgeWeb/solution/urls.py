'''
Created on 2012-7-25

@author: TheBeet
'''
from django.conf.urls.defaults import patterns, url, include

from views import SubmitSolutionView, SolutionListView, SolutionDetailView, SolutionCompareView

urlpatterns = patterns('',
    url(r'^submit/(?P<problem>\d+)/$', SubmitSolutionView.as_view(), name="submit"),
    url(r'^(?P<pk>\d+)/$', SolutionDetailView.as_view(), name="detail"),
    url(r'^$', SolutionListView.as_view(), name="list"),
    url(r'^compare/(?P<user1>\w+)-(?P<user2>\w+)', SolutionCompareView.as_view(), name="compare"),
    url(r'^compare/$', SolutionCompareView.as_view(), name="compare"),
)

