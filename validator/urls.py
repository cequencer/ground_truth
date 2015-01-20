from django.conf.urls import patterns, include, url

urlpatterns = patterns('validator.views',

    # url(r'^page/$', 'index', name='index'),
    # url(r'^page/(?P<pagination>\d+)$', 'index', name='index'),
    # url(r'^align/(?P<record_id>\d+)$', 'align', name='align'),
    url(r'^$', 'index', name='index'),
    url(r'^stat/(?P<researcher>\w+)$', 'stat', name='stat'),
    url(r'^change_mode$', 'change_mode', name='change_mode'),
)
