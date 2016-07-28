from django.conf.urls import url

from core.ofm_views import PlayerDetailView, PlayerDataView, PlayerDataAsJsonView, FinanceDataView

app_name = 'ofm'
urlpatterns = [
    url(r'^player_statistics/?$', PlayerDataView.as_view(), name='player_statistics'),
    url(r'^player_statistics_json/?$', PlayerDataAsJsonView.as_view(), name='player_statistics_json'),
    url(r'^players/(?P<pk>[0-9]+)/?$', PlayerDetailView.as_view(), name='player_detail'),
    url(r'^finances/?$', FinanceDataView.as_view(), name='finance_overview'),
]
