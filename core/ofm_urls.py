from django.conf.urls import url

from core.ofm_views import PlayerDetailView, PlayerStatisticsView, PlayerStatisticsAsJsonView, FinanceDataView, \
    FinancesAsJsonView, MatchesView, MatchesAsJsonView, StadiumStatisticsView, StadiumStatisticsAsJsonView, \
    StadiumDetailView, StadiumStandStatisticsView, FinanceIncomeChartView, FinanceExpensesChartView

app_name = 'ofm'
urlpatterns = [
    url(r'^player_statistics/?$', PlayerStatisticsView.as_view(), name='player_statistics'),
    url(r'^player_statistics_json/?$', PlayerStatisticsAsJsonView.as_view(), name='player_statistics_json'),
    url(r'^players/(?P<pk>[0-9]+)/?$', PlayerDetailView.as_view(), name='player_detail'),
    url(r'^finances/?$', FinanceDataView.as_view(), name='finance_overview'),
    url(r'^finances_json/?$', FinancesAsJsonView.as_view(), name='finances_json'),
    url(r'^finances_income_chart_json/?$', FinanceIncomeChartView.as_view(), name='finances_income_chart_json'),
    url(r'^finances_expenses_chart_json/?$', FinanceExpensesChartView.as_view(), name='finances_expenses_chart_json'),
    url(r'^matches/?$', MatchesView.as_view(), name='matches_overview'),
    url(r'^matches_json/?$', MatchesAsJsonView.as_view(), name='matches_overview_json'),
    url(r'^stadium_statistics/?$', StadiumStatisticsView.as_view(), name='stadium_statistics_overview'),
    url(r'^stadium_statistics_json/?$', StadiumStatisticsAsJsonView.as_view(), name='stadium_statistics_overview_json'),
    url(r'^stadium/(?P<pk>[0-9]+)/?$', StadiumDetailView.as_view(), name='stadium_detail'),
    url(r'^stadium_stand/(?P<sector>\w+)?$', StadiumStandStatisticsView.as_view(), name='stadium_stand_statistics'),
]
