from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from views import IndexView

urlpatterns = patterns('newjudge',
    # Examples:
    url(r'^$', IndexView.as_view(), name='home'),
    url(r'^problem/', include('JudgeWeb.problem.urls', namespace = 'problem')),
    url(r'^user/', include('JudgeWeb.user.urls', namespace = 'user')),
    url(r'^solution/', include('JudgeWeb.solution.urls', namespace = 'solution')),
    url(r'^contest/', include('JudgeWeb.contest.urls', namespace = 'contest')),
    url(r'^diary/', include('JudgeWeb.diary.urls', namespace = 'diary')),
    url(r'^discuss/', include('JudgeWeb.discuss.urls', namespace = 'discuss')),
    url(r'^mail/', include('JudgeWeb.mail.urls', namespace = 'mail')),
    url(r'^dashboard/', include('JudgeWeb.dashboard.urls', namespace = 'dashboard')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += staticfiles_urlpatterns()
