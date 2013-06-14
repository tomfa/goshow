#set encoding=utf-8
from django.conf.urls.defaults import *
from go import views

urlpatterns = patterns(
    '',
    url(r'^/?$', views.index, name='index'),
    # r = regex: ^: start, $: end,
    url(r'^view/(?P<key>\d+)/$', views.get_list, name='listview'),
    url('^view/$', views.get_all_lists, name='all-listview'),
    url('^operate/$', views.operation, name='ajax-operations'),
    url('^register/$', views.register, name='register'),
    url('^demo/$', views.demo, name='demo'),
    # url(r'^edit$', views.edit, name='edit'),
)
