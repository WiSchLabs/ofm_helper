import core.ofm_views
from core import views
from core.ofm_views import PlayerDetailView, PlayerDataView, PlayerDataAsJsonView
from django.conf.urls import url

app_name = 'ofm'
urlpatterns = [
    url(r'^player_statistics/?$', core.ofm_views.test_chart_view, name='player_statistics'),
    url(r'^player_data/?$', PlayerDataView.as_view(), name='player_data'),
    url(r'^player_data_json/?$', PlayerDataAsJsonView.as_view(), name='player_data_json'),
    url(r'^players/(?P<pk>[0-9]+)/?$', PlayerDetailView.as_view(), name='player_detail'),
]
