from braces.views import CsrfExemptMixin, JsonRequestResponseMixin
from chartit import DataPool, Chart
from core.models import Player, Contract, PlayerStatistics
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, TemplateView, View


@method_decorator(login_required, name='dispatch')
class PlayerDataView(TemplateView):
    template_name = 'core/ofm/player_data.html'


@method_decorator(login_required, name='dispatch')
class PlayerDataAsJsonView(CsrfExemptMixin, JsonRequestResponseMixin, View):

    def get(self, request, *args, **kwargs):
        contracts = Contract.objects.filter(user=self.request.user, sold_on_matchday=None)
        players = [contract.player for contract in contracts]

        show_diff = self.request.GET.get('show_diff', default='false').lower() == 'true'

        player_data_json = [self._get_last_two_statistics_diff(player, show_diff) for player in players]

        return self.render_json_response(player_data_json)

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

    def get_object(self):
        player = super(PlayerDetailView, self).get_object()
        contracts = Contract.objects.filter(user=self.request.user, player=player, sold_on_matchday=None)
        return player if contracts.count() > 0 else None


def test_chart_view(request):
    # Step 1: Create a DataPool with the data we want to retrieve.
    statistics_data = \
        DataPool(
                series=
                [{'options': {
                    'source': PlayerStatistics.objects.all()},
                    'terms': [
                        'player__name',
                        'ep',
                        'tp',
                        'awp']}
                ])

    # Step 2: Create the Chart object
    chart = Chart(
            datasource=statistics_data,
            series_options=
            [{'options': {
                'type': 'column',
                'stacking': False},
                'terms': {'player__name': ['ep', 'tp', 'awp', ]}
            }],
            chart_options=
            {
                'title': {
                    'text': 'Player statistics'},
            })

    # Step 3: Send the chart object to the template.
    context = RequestContext(request)
    context['chart'] = chart

    return render_to_response('core/ofm/single_chart.html', context)