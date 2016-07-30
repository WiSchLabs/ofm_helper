import logging

from braces.views import CsrfExemptMixin, JsonRequestResponseMixin
from chartit import DataPool, Chart
from core.models import Player, Contract, PlayerStatistics, Finance, Matchday
from django.contrib.auth.decorators import login_required
from django.core.exceptions import MultipleObjectsReturned
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, TemplateView, View


@method_decorator(login_required, name='dispatch')
class PlayerStatisticsView(TemplateView):
    template_name = 'core/ofm/player_statistics.html'

    def get_context_data(self, **kwargs):
        context = super(PlayerStatisticsView, self).get_context_data(**kwargs)

        matchdays = Matchday.objects.filter(player_statistics__isnull=False).distinct()

        context['matchdays'] = matchdays

        return context


@method_decorator(login_required, name='dispatch')
class PlayerStatisticsAsJsonView(CsrfExemptMixin, JsonRequestResponseMixin, View):

    def get(self, request, *args, **kwargs):
        contracts = Contract.objects.filter(user=self.request.user, sold_on_matchday=None)
        players = [contract.player for contract in contracts]

        newer_matchday_season = self.request.GET.get('newer_matchday_season', default=Matchday.objects.all()[0].season.number)
        newer_matchday = self.request.GET.get('newer_matchday', default=Matchday.objects.all()[0].number)
        older_matchday_season = self.request.GET.get('older_matchday_season', default=Matchday.objects.all()[1].season.number if Matchday.objects.all().count() > 1 else None)
        older_matchday = self.request.GET.get('older_matchday', default=Matchday.objects.all()[1].number if Matchday.objects.all().count() > 1 else None)

        show_diff = self.request.GET.get('show_diff', default='false').lower() == 'true'

        player_statistics_tuples = [self._get_statistics_from_player_and_matchday(player,
                                                                            newer_matchday_season, newer_matchday,
                                                                            older_matchday_season, older_matchday)
                             for player in players]

        player_statistics_json = [self._get_player_statistics_diff_in_json(newer_player_statistic,
                                                                           older_player_statistic, show_diff)
                                  for (newer_player_statistic, older_player_statistic) in player_statistics_tuples]

        return self.render_json_response(player_statistics_json)

    def _get_statistics_from_player_and_matchday(self, player,
                                                 newer_matchday_season, newer_matchday,
                                                 older_matchday_season, older_matchday):

        ps1 = PlayerStatistics.objects.filter(player=player, matchday__season__number=newer_matchday_season, matchday__number=newer_matchday)
        ps2 = PlayerStatistics.objects.filter(player=player, matchday__season__number=older_matchday_season, matchday__number=older_matchday)

        ps1 = self._validate_filtered_player_statistics(ps1)
        ps2 = self._validate_filtered_player_statistics(ps2)

        return ps1, ps2

    def _validate_filtered_player_statistics(self, player_statistics):
        if len(player_statistics) > 1:
            raise MultipleObjectsReturned
        elif player_statistics:
            player_statistics = player_statistics[0]
        return player_statistics

    def _get_player_statistics_diff_in_json(self, newer_player_statistics, older_player_statistics, show_diff=True):
        """
        Args:
            newer_player_statistics: newer statistic
            older_player_statistics: older statistic

        Returns:
            A dictionary of player statistics data. If st2 is None st1 is returned
        """

        if not newer_player_statistics:
            newer_player_statistics = PlayerStatistics.objects.all()[0]

        ep = newer_player_statistics.ep
        if show_diff and older_player_statistics:
            ep = newer_player_statistics.ep - older_player_statistics.ep
        tp = newer_player_statistics.tp
        if show_diff and older_player_statistics:
            tp = newer_player_statistics.tp - older_player_statistics.tp
        awp = newer_player_statistics.awp
        if show_diff and older_player_statistics:
            awp = newer_player_statistics.awp - older_player_statistics.awp
        freshness = newer_player_statistics.freshness
        if show_diff and older_player_statistics:
            freshness = newer_player_statistics.freshness - older_player_statistics.freshness

        statistic_diff = dict()
        statistic_diff['position'] = newer_player_statistics.player.position
        statistic_diff['age'] = newer_player_statistics.age
        statistic_diff['strength'] = newer_player_statistics.strength
        statistic_diff['name'] = '<a href="%s">%s</a>' % (newer_player_statistics.player.get_absolute_url(), newer_player_statistics.player.name)
        statistic_diff['ep'] = ep
        statistic_diff['tp'] = tp
        statistic_diff['awp'] = awp
        statistic_diff['freshness'] = freshness
        statistic_diff['games_in_season'] = newer_player_statistics.games_in_season
        statistic_diff['goals_in_season'] = newer_player_statistics.goals_in_season
        statistic_diff['won_tacklings_in_season'] = newer_player_statistics.won_tacklings_in_season
        statistic_diff['lost_tacklings_in_season'] = newer_player_statistics.lost_tacklings_in_season
        statistic_diff['won_friendly_tacklings_in_season'] = newer_player_statistics.won_friendly_tacklings_in_season
        statistic_diff['lost_friendly_tacklings_in_season'] = newer_player_statistics.lost_friendly_tacklings_in_season
        statistic_diff['yellow_cards_in_season'] = newer_player_statistics.yellow_cards_in_season
        statistic_diff['red_cards_in_season'] = newer_player_statistics.red_cards_in_season
        statistic_diff['equity'] = newer_player_statistics.equity

        return statistic_diff


@method_decorator(login_required, name='dispatch')
class PlayerDetailView(DetailView):
    context_object_name = 'player'
    template_name = 'core/ofm/player_detail.html'
    queryset = Player.objects.all()

    def get_context_data(self, **kwargs):
        context = super(PlayerDetailView, self).get_context_data(**kwargs)

        player = self.get_object()

        statistics_data = DataPool(
            series=[
                {'options':
                    {'source': PlayerStatistics.objects.filter(player=player)},
                    'terms': [
                        'matchday__number',
                        'ep',
                        'tp',
                        'awp'
                    ]
                }
            ]
        )

        chart = Chart(
            datasource=statistics_data,
            series_options=
            [{'options': {
                'type': 'spline',
                'stacking': False},
                'terms': {'matchday__number': ['ep', 'tp', 'awp', ]}
            }],
            chart_options=
            {
                'title': {
                    'text': 'Spielerstatistik'
                },
                'xAxis': {
                    'title': {
                       'text': 'Spieltag'}
                },
                'yAxis': {
                    'title': {
                       'text': ' '}
                },
            }
        )

        context['chart'] = chart

        return context

    def get_object(self):
        player = super(PlayerDetailView, self).get_object()
        contracts = Contract.objects.filter(user=self.request.user, player=player, sold_on_matchday=None)
        return player if contracts.count() > 0 else None


@method_decorator(login_required, name='dispatch')
class FinanceDataView(TemplateView):
    template_name = 'core/ofm/finances.html'

    def get_context_data(self, **kwargs):
        context = super(FinanceDataView, self).get_context_data(**kwargs)

        logger = logging.getLogger(__name__)

        logger.debug('debug')
        logger.info('info')
        logger.warning('warning')
        logger.error('error')
        logger.critical('critical')

        finance_data = DataPool(
            series=[
                {'options':
                    {'source': Finance.objects.filter(user=self.request.user)},
                    'terms': [
                        'matchday__number',
                        'balance',
                    ]
                }
            ]
        )

        chart = Chart(
            datasource=finance_data,
            series_options=
            [{'options': {
                    'type': 'spline',
                    'stacking': False,
                    'allowPointSelect': True,
                },
                'terms': {'matchday__number': ['balance', ]}
            }],
            chart_options=
            {
                'title': {
                    'text': 'Finanzstatistik'
                },
                'xAxis': {
                    'title': {
                       'text': 'Spieltag'}
                },
                'yAxis': {
                    'title': {
                       'text': ' '}
                },
            }
        )

        context['chart'] = chart

        return context


@method_decorator(login_required, name='dispatch')
class FinanceDataColumnChartView(TemplateView):
    template_name = 'core/ofm/finances.html'

    def get_context_data(self, **kwargs):
        context = super(FinanceDataColumnChartView, self).get_context_data(**kwargs)

        finance_data = DataPool(
            series=[
                {'options':
                    {'source': Finance.objects.filter(user=self.request.user)},
                    'terms': [
                        'matchday__number',
                        'balance',
                        'income_visitors_league',
                        'income_sponsoring',
                        'income_cup',
                        'income_interests',
                        'income_loan',
                        'income_transfer',
                        'income_visitors_friendlies',
                        'income_friendlies',
                        'income_funcup',
                        'income_betting',
                        'expenses_player_salaries',
                        'expenses_stadium',
                        'expenses_youth',
                        'expenses_interests',
                        'expenses_trainings',
                        'expenses_transfer',
                        'expenses_compensation',
                        'expenses_friendlies',
                        'expenses_funcup',
                        'expenses_betting',
                    ]
                }
            ]
        )

        chart = Chart(
            datasource=finance_data,
            series_options=
            [
                {'options': {
                        'type': 'column',
                        'stacking': True,
                        'stack': 0,
                    },
                    'terms': {'matchday__number': [
                                'income_visitors_league',
                                'income_sponsoring',
                                'income_cup',
                                'income_interests',
                                'income_loan',
                                'income_transfer',
                                'income_visitors_friendlies',
                                'income_friendlies',
                                'income_funcup',
                                'income_betting']}
                },
                {'options': {
                        'type': 'column',
                        'stacking': True,
                        'stack': 1,
                    },
                    'terms': {'matchday__number': [
                                'expenses_player_salaries',
                                'expenses_stadium',
                                'expenses_youth',
                                'expenses_interests',
                                'expenses_trainings',
                                'expenses_transfer',
                                'expenses_compensation',
                                'expenses_friendlies',
                                'expenses_funcup',
                                'expenses_betting']}
                }
            ],
            chart_options=
            {
                'title': {
                    'text': 'Finanzstatistik'
                },
                'xAxis': {
                    'title': {
                       'text': 'Spieltag'}
                },
                'yAxis': {
                    'title': {
                       'text': ' '}
                },
            }
        )

        context['chart'] = chart

        return context
