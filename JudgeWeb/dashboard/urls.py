'''
Created on 2012-9-13

@author: Macro
'''
from django.conf.urls.defaults import patterns, url, include

from views import DashBoardView

urlpatterns = patterns('',
    url(r'^$', DashBoardView.as_view(), name="dashboard"),
    url(r'^(?P<beg>\d+)-(?P<end>\d+)', DashBoardView.as_view(), name="daterange"),
)