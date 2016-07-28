from braces.views import CsrfExemptMixin, JsonRequestResponseMixin
from chartit import DataPool, Chart
from core.models import Player, Contract, PlayerStatistics, Finance, Matchday
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, TemplateView, View


@method_decorator(login_required, name='dispatch')
class PlayerStatisticsView(TemplateView):
    template_name = 'core/ofm/player_statistics.html'

    def get_context_data(self, **kwargs):
        context = super(PlayerStatisticsView, self).get_context_data(**kwargs)

        #contracts = Contract.objects.filter(user=self.request.user, sold_on_matchday=None)
        #players = [contract.player for contract in contracts]

        #player_statistics = [PlayerStatistics.objects.filter(player=player) for player in players]
        #player_statistics = [item for sublist in player_statistics for item in sublist]

        #matchdays = list(set([player_statistic.matchday for player_statistic in player_statistics]))

        matchdays = Matchday.objects.filter(player_statistics__isnull=False).distinct()

        context['matchdays'] = matchdays

        return context


@method_decorator(login_required, name='dispatch')
class PlayerStatisticsAsJsonView(CsrfExemptMixin, JsonRequestResponseMixin, View):

    def get(self, request, *args, **kwargs):
        contracts = Contract.objects.filter(user=self.request.user, sold_on_matchday=None)
        players = [contract.player for contract in contracts]

        show_diff = self.request.GET.get('show_diff', default='false').lower() == 'true'

        player_statistics_json = [self._get_last_two_statistics_diff(player, show_diff) for player in players]

        return self.render_json_response(player_statistics_json)

    def _get_last_two_statistics_diff(self, player, show_diff=True):
        size = player.statistics.all().count()
        st1 = player.statistics.all()[size - 1]
        if size > 1:
            st2 = player.statistics.all()[size - 2]
            return self._player_statistics_diff(st1, st2, show_diff)
        else:
            return self._player_statistics_diff(st1, None, show_diff)

    def _player_statistics_diff(self, st1: PlayerStatistics, st2: PlayerStatistics, show_diff=True):
        """
        Args:
            st1: later statistic
            st2: former statistic

        Returns:
            A dictionary of player statistics data. If st2 is None st1 is returned
        """
        ep = st1.ep
        if show_diff and st2:
            ep = st1.ep - st2.ep
        tp = st1.tp
        if show_diff and st2:
            tp = st1.tp - st2.tp
        awp = st1.awp
        if show_diff and st2:
            awp = st1.awp - st2.awp
        freshness = st1.freshness
        if show_diff and st2:
            freshness = st1.freshness - st2.freshness

        statistic_diff = dict()
        statistic_diff['position'] = st1.player.position
        statistic_diff['age'] = st1.age
        statistic_diff['strength'] = st1.strength
        statistic_diff['name'] = '<a href="%s">%s</a>' % (st1.player.get_absolute_url(), st1.player.name)
        statistic_diff['ep'] = ep
        statistic_diff['tp'] = tp
        statistic_diff['awp'] = awp
        statistic_diff['freshness'] = freshness
        statistic_diff['games_in_season'] = st1.games_in_season
        statistic_diff['goals_in_season'] = st1.goals_in_season
        statistic_diff['won_tacklings_in_season'] = st1.won_tacklings_in_season
        statistic_diff['lost_tacklings_in_season'] = st1.lost_tacklings_in_season
        statistic_diff['won_friendly_tacklings_in_season'] = st1.won_friendly_tacklings_in_season
        statistic_diff['lost_friendly_tacklings_in_season'] = st1.lost_friendly_tacklings_in_season
        statistic_diff['yellow_cards_in_season'] = st1.yellow_cards_in_season
        statistic_diff['red_cards_in_season'] = st1.red_cards_in_season
        statistic_diff['equity'] = st1.equity

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
                'stacking': False},
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
