from django.conf.urls import patterns, include, url

urlpatterns = patterns('record.views',

    url(r'^page/$', 'index', name='index'),
    url(r'^page/(?P<pagination>\d+)$', 'index', name='index'),
    url(r'^align/(?P<record_id>\d+)$', 'align', name='align'),
    url(r'^update_label$', 'update_label', name='update_label'),
    url(r'^select_name$', 'select_name', name='select_name'),
    url(r'^select_name_dl$', 'select_name_dl', name='select_name_dl'),
    url(r'^clear_labels$', 'clear_labels', name='clear_labels'),
)
