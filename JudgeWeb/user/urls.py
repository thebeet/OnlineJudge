'''
Created on 2012-7-25

@author: TheBeet
'''
from django.conf.urls.defaults import patterns, url

from views import ajax_login, ajax_logout, UserDetailView, UserRankView, UserStatisticView, RegisterView

urlpatterns = patterns('',
    url(r'^login/$', ajax_login, name="login"),
    url(r'^logout/$', ajax_logout, name="logout"),
    url(r'^profile/(?P<slug>\w+)/$', UserDetailView.as_view(), name="detail"),
    url(r'^statistic/(?P<slug>\w+)/$', UserStatisticView.as_view(), name="statistic"),
    url(r'^rank/$', UserRankView.as_view(), name="rank"),
    url(r'^register/$', RegisterView.as_view(), name="register"),
)

