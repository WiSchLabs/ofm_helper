from django.conf.urls import url

from core.ofm_views import PlayerDetailView, PlayerStatisticsView, PlayerStatisticsAsJsonView, FinanceDataView, \
    FinancesAsJsonView

app_name = 'ofm'
urlpatterns = [
    url(r'^player_statistics/?$', PlayerStatisticsView.as_view(), name='player_statistics'),
    url(r'^player_statistics_json/?$', PlayerStatisticsAsJsonView.as_view(), name='player_statistics_json'),
    url(r'^players/(?P<pk>[0-9]+)/?$', PlayerDetailView.as_view(), name='player_detail'),
    url(r'^finances/?$', FinanceDataView.as_view(), name='finance_overview'),
    url(r'^finances_json/?$', FinancesAsJsonView.as_view(), name='finances_json'),
]
