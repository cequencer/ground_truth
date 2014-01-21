from django.conf.urls import patterns, include, url

urlpatterns = patterns('record.views',

    url(r'^$', 'index', name='index'),
    url(r'^(?P<record_id>\d+)$', 'align', name='align'),
    url(r'^update_label$', 'update_label', name='update_label'),
    url(r'^select_name$', 'select_name', name='select_name'),
    url(r'^clear_labels$', 'clear_labels', name='clear_labels'),
)
