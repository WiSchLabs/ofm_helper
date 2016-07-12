from braces.views import CsrfExemptMixin, JsonRequestResponseMixin
from core.models import Player, Contract, PlayerStatistics
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, TemplateView, View


@method_decorator(login_required, name='dispatch')
class PlayerListView(ListView):
    context_object_name = 'player_list'
    template_name = 'core/ofm/player_list.html'

    def get_queryset(self):
        contracts = Contract.objects.filter(user=self.request.user, sold_on_matchday=None)
        return [contract.player for contract in contracts]


@method_decorator(login_required, name='dispatch')
class PlayerDataView(TemplateView):
    template_name = 'core/ofm/player_data.html'


@method_decorator(login_required, name='dispatch')
class PlayerDataAsJsonView(CsrfExemptMixin, JsonRequestResponseMixin, View):
    def get(self, request, *args, **kwargs):
        contracts = Contract.objects.filter(user=self.request.user, sold_on_matchday=None)
        players = [contract.player for contract in contracts]

        player_data_json = [self._get_last_two_statistics_diff(player) for player in players]

        return self.render_json_response(player_data_json)

    def _get_last_two_statistics_diff(self, player):
        size = player.statistics.all().count()
        st1 = player.statistics.all()[size - 1]
        if size > 1:
            st2 = player.statistics.all()[size - 2]
            return self._player_statistics_diff(st1, st2)
        else:
            return self._player_statistics_diff(st1, None)

    def _player_statistics_diff(self, st1: PlayerStatistics, st2: PlayerStatistics):
        """
        Args:
            st1: later statistic
            st2: former statistic

        Returns:
            A dictionary of player statistics data. If st2 is None st1 is returned
        """

        statistic_diff = dict()
        statistic_diff['position'] = st1.player.position
        statistic_diff['name'] = st1.player.name
        statistic_diff['ep'] = st1.ep - st2.ep if st2 else st1.ep
        statistic_diff['tp'] = st1.tp - st2.tp if st2 else st1.tp
        statistic_diff['awp'] = st1.awp - st2.awp if st2 else st1.awp
        statistic_diff['strength'] = st1.strength - st2.strength if st2 else st1.strength
        statistic_diff['freshness'] = st1.freshness - st2.freshness if st2 else st1.freshness
        statistic_diff['games_in_season'] = st1.games_in_season - st2.games_in_season if st2 else st1.games_in_season
        statistic_diff['goals_in_season'] = st1.goals_in_season - st2.goals_in_season if st2 else st1.goals_in_season
        statistic_diff['won_tacklings_in_season'] = st1.won_tacklings_in_season - st2.won_tacklings_in_season if st2 else st1.won_tacklings_in_season
        statistic_diff['lost_tacklings_in_season'] = st1.lost_tacklings_in_season - st2.lost_tacklings_in_season if st2 else st1.lost_tacklings_in_season
        statistic_diff['won_friendly_tacklings_in_season'] = st1.won_friendly_tacklings_in_season - st2.won_friendly_tacklings_in_season if st2 else st1.won_friendly_tacklings_in_season
        statistic_diff['lost_friendly_tacklings_in_season'] = st1.lost_friendly_tacklings_in_season - st2.lost_friendly_tacklings_in_season if st2 else st1.lost_friendly_tacklings_in_season
        statistic_diff['yellow_cards_in_season'] = st1.yellow_cards_in_season - st2.yellow_cards_in_season if st2 else st1.yellow_cards_in_season
        statistic_diff['red_cards_in_season'] = st1.red_cards_in_season - st2.red_cards_in_season if st2 else st1.red_cards_in_season
        statistic_diff['equity'] = st1.equity - st2.equity if st2 else st1.equity

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
