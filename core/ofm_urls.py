from django.conf.urls import url

from core.views.ofm import plotting_views
from core.views.ofm.base_views import GetCurrentMatchdayView
from core.views.ofm.finance_views import FinanceBalanceChartView, FinanceDataView, FinanceExpensesChartView, \
                                         FinanceIncomeChartView, FinancesAsJsonView
from core.views.ofm.match_views import MatchesAsJsonView, MatchesSummaryJsonView, MatchesView
from core.views.ofm.player_views import PlayerChartView, PlayerDetailView, PlayerStatisticsAsJsonView, \
                                        PlayerStatisticsView
from core.views.ofm.stadium_views import StadiumDetailView, StadiumStandStatisticsChartView, \
                                         StadiumStandStatisticsView, StadiumStatisticsAsJsonView, StadiumStatisticsView

app_name = 'ofm'

urlpatterns = [
    url(r'^player_statistics/?$', PlayerStatisticsView.as_view(), name='player_statistics'),
    url(r'^player_statistics_json/?$', PlayerStatisticsAsJsonView.as_view(), name='player_statistics_json'),
    url(r'^players/(?P<pk>[0-9]+)/?$', PlayerDetailView.as_view(), name='player_detail'),
    url(r'^players_chart_json/?$', PlayerChartView.as_view(), name='players_chart_json'),

    url(r'^finances/?$', FinanceDataView.as_view(), name='finance_overview'),
    url(r'^finances_json/?$', FinancesAsJsonView.as_view(), name='finances_json'),
    url(r'^finances_balance_chart_json/?$', FinanceBalanceChartView.as_view(), name='finances_balance_chart_json'),
    url(r'^finances_income_chart_json/?$', FinanceIncomeChartView.as_view(), name='finances_income_chart_json'),
    url(r'^finances_expenses_chart_json/?$', FinanceExpensesChartView.as_view(), name='finances_expenses_chart_json'),

    url(r'^matches/?$', MatchesView.as_view(), name='matches_overview'),
    url(r'^matches_json/?$', MatchesAsJsonView.as_view(), name='matches_overview_json'),
    url(r'^matches_summary_json/?$', MatchesSummaryJsonView.as_view(), name='matches_summary_json'),

    url(r'^stadium_statistics/?$', StadiumStatisticsView.as_view(), name='stadium_statistics_overview'),
    url(r'^stadium_statistics_json/?$', StadiumStatisticsAsJsonView.as_view(), name='stadium_statistics_overview_json'),
    url(r'^stadium/(?P<pk>[0-9]+)/?$', StadiumDetailView.as_view(), name='stadium_detail'),
    url(r'^stadium_stand/?$', StadiumStandStatisticsView.as_view(), name='stadium_stand_statistics'),
    url(r'^stadium_stand_chart_json/?$', StadiumStandStatisticsChartView.as_view(),
        name='stadium_stand_statistics_chart_json'),

    url(r'^get_current_matchday/?$', GetCurrentMatchdayView.as_view(), name='get_current_matchday'),

    url(r'^foobar/?$', plotting_views.render_plot, name='plot'),
]
