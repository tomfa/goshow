#set encoding=utf-8
from django.conf.urls.defaults import *
from go import views

urlpatterns = patterns(
    '',
    url(r'^/?$', views.index, name='index'),
    # r = regex: ^: start, $: end,
    url(r'view/^(?P<list_name>[\wæøå ._0-9-]+)$', views.get_list, name='listview'),
    url('view/$', views.get_all_lists, name='all-listview'),
    url('operate/$', views.operation, name='ajax-operations'),
    # url(r'^edit$', views.edit, name='edit'),
)
