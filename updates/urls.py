from django.conf.urls import patterns, include, url


urlpatterns = patterns('updates.views',
	url(r'^$', 'index', name='margarita_index'),
    url(r'^update_list/$', 'update_list', name='margarita_update_list'),
    url(r'^process_queue/$', 'process_queue', name='margarita_process_queue'),
)