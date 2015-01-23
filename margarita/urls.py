from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^', include('updates.urls')),
    url(r'^updates/', include('updates.urls')),

    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('django.contrib.auth.views',
    url(r'^login/$', 'login', {'template_name': 'login.html'},
        name='login'),
    url(r'^logout/$', 'logout', {'next_page': '/'}, name='logout'),
)
