from django.conf.urls import patterns, include, url


urlpatterns = patterns('updates.views',
    url(r'^$', 'update_list', name='margarita_update_list'),
)