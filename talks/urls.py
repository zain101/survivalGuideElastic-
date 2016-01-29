from __future__ import absolute_import

from django.conf.urls import url, patterns, include
from . import views


list_patterns = patterns(
    '',
    # url(r'^$', views.TalkListDetailView.as_view(), name='detail'),
    url(r'^$', views.TalkListListView.as_view(), name='list'),
    url(r'^d/(?P<slug>[-\w]+)/$',
        views.TalkListDetailView.as_view(), name='detail'),
    url(r'^create/$', views.TalkListCreateView.as_view(), name='create'),
    url(r'^e/(?P<slug>[-\w]+)/$',
        views.TalkListUpdateView.as_view(), name='update'),
    url(r'^remove/(?P<talklist_pk>\d+)/(?P<pk>\d+)/$',
        views.TalkListRemoveTalkView.as_view(),
        name='remove_talk'),
    url(r'^s/(?P<slug>[-\w]+)/$', views.TalkListScheduleView.as_view(),
        name='schedule'),
    url(r'^search/?$', views.MySearchView.as_view(), name='search_view'),
    url(r'^search_auto/?$', views.autocomplete, name='search_auto'),
    url(r'^search_auto_temp/?$', views.MyAutoSearchView.as_view(), name='search_auto_temp'),

)

urlpatterns = patterns(
    '',
    url(r'^lists/', include(list_patterns, namespace='lists'))
)
