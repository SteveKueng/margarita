from django.conf.urls import patterns, include, url


urlpatterns = patterns('updates.views',
	url(r'^$', 'index', name='margarita_index'),
    url(r'^update_list/$', 'update_list', name='margarita_update_list'),
    url(r'^process_queue/$', 'process_queue', name='margarita_process_queue'),
    url(r'^add_all/(?P<branchname>[^/]+)/$', 'add_all', name='margarita_add_all'),
    url(r'^dup/(?P<frombranch>[^/]+)/(?P<tobranch>[^/]+)/$', 'dup', name='margarita_dup'),
    url(r'^delete_branch/(?P<branchname>[^/]+)/$', 'delete_branch', name='margarita_delete_branch'),
    url(r'^new_branch/(?P<branchname>[^/]+)/$', 'new_branch', name='margarita_new_branch'),
)