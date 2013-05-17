'''
Created on 2012-8-31

@author: Macro
'''

from django.conf.urls.defaults import patterns, url, include

from views import DiaryView

urlpatterns = patterns('',
    url(r'^$', DiaryView.as_view(), name="list"),
)