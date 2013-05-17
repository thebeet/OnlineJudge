'''
Created on 2012-9-7

@author: Macro
'''
from django.conf.urls.defaults import patterns, url
from views import MailInboxView, MailDetialView, MailOutboxView, MailChatView

urlpatterns = patterns('',
    url(r'^inbox/$', MailInboxView.as_view(), name="inbox"),
    url(r'^outbox/$', MailOutboxView.as_view(), name="outbox"),
    url(r'^(?P<pk>\d+)/$', MailDetialView.as_view(), name="detail"),
    url(r'^chat/(?P<user>\w+)/$', MailChatView.as_view(), name="chat"),
)
