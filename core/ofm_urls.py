from core.ofm_views import PlayerListView, PlayerDetailView
from django.conf.urls import url

from core import views

app_name = 'ofm'
urlpatterns = [
    url(r'^player_statistics/?$', views.test_chart_view, name='player_statistics'),
    url(r'^players/?$', PlayerListView.as_view(), name='player_list'),
    url(r'^players/(?P<pk>[0-9]+)/?$', PlayerDetailView.as_view(), name='player_detail'),
]
