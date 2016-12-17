from braces.views import CsrfExemptMixin, JsonRequestResponseMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import TemplateView, DetailView

from core.models import Matchday, Contract, PlayerStatistics, AwpBoundaries, Player
from core.views.view_utils import validate_filtered_field


@method_decorator(login_required, name='dispatch')
class PlayerStatisticsView(TemplateView):
    template_name = 'core/ofm/player_statistics.html'

    def get_context_data(self, **kwargs):
        matchdays = Matchday.objects.filter(player_statistics__isnull=False).distinct()

        context = super(PlayerStatisticsView, self).get_context_data(**kwargs)
        context['matchdays'] = matchdays
        context['players_count'] = Contract.objects.filter(user=self.request.user, sold_on_matchday=None).count()

        return context


@method_decorator(login_required, name='dispatch')
class PlayerStatisticsAsJsonView(CsrfExemptMixin, JsonRequestResponseMixin, View):
    def get(self, request):
        contracts = Contract.objects.filter(user=request.user, sold_on_matchday=None)
        players = [contract.player for contract in contracts]
        current_matchday = Matchday.objects.all()[0]

        newer_matchday_season = request.GET.get('newer_matchday_season', default=current_matchday.season.number)
        newer_matchday = request.GET.get('newer_matchday', default=current_matchday.number)
        older_matchday_season = request.GET.get('older_matchday_season')
        older_matchday = request.GET.get('older_matchday')
        diff_mode_enabled = older_matchday and older_matchday_season

        player_statistics_tuples = []
        for player in players:
            newer_player_statistics, older_player_statistics = self._get_statistics_from_player_and_matchday(
                player,
                newer_matchday_season, newer_matchday,
                older_matchday_season, older_matchday
            )
            if newer_player_statistics and (older_player_statistics or not diff_mode_enabled):
                player_statistics_tuples.append((newer_player_statistics, older_player_statistics))

        player_statistics_json = [
            self._get_player_statistics_diff_in_json(newer_player_statistics, older_player_statistics)
            for (newer_player_statistics, older_player_statistics) in player_statistics_tuples
        ]

        return self.render_json_response(player_statistics_json)

    @staticmethod
    def _get_statistics_from_player_and_matchday(player,
                                                 newer_matchday_season, newer_matchday,
                                                 older_matchday_season, older_matchday):

        newer_player_statistics = PlayerStatistics.objects.filter(
            player=player,
            matchday__season__number=newer_matchday_season,
            matchday__number=newer_matchday
        )
        older_player_statistics = PlayerStatistics.objects.filter(
            player=player,
            matchday__season__number=older_matchday_season,
            matchday__number=older_matchday
        )

        newer_player_statistics = validate_filtered_field(newer_player_statistics)
        older_player_statistics = validate_filtered_field(older_player_statistics)

        if not newer_player_statistics:
            newer_player_statistics = PlayerStatistics.objects.filter(
                player=player,
                matchday__season__number=newer_matchday_season
            ).order_by('matchday')[0]

        return newer_player_statistics, older_player_statistics

    @staticmethod
    def _get_player_statistics_diff_in_json(newer_player_statistics, older_player_statistics):
        """
        Args:
            newer_player_statistics: newer statistic
            older_player_statistics: older statistic

        Returns:
            A dictionary of player statistics data. If st2 is None st1 is returned
        """

        strength = newer_player_statistics.strength
        if older_player_statistics:
            strength = newer_player_statistics.strength - older_player_statistics.strength
        ep = newer_player_statistics.ep
        if older_player_statistics:
            ep = newer_player_statistics.ep - older_player_statistics.ep
        tp = newer_player_statistics.tp
        if older_player_statistics:
            tp = newer_player_statistics.tp - older_player_statistics.tp
        awp = newer_player_statistics.awp
        if older_player_statistics:
            awp = newer_player_statistics.awp - older_player_statistics.awp
        freshness = newer_player_statistics.freshness
        if older_player_statistics:
            freshness = newer_player_statistics.freshness - older_player_statistics.freshness

        awp_boundaries = AwpBoundaries.get_from_matchday(newer_player_statistics.matchday)
        awp_to_next_bound = awp_boundaries[newer_player_statistics.strength + 1] - newer_player_statistics.awp

        statistic_diff = dict()
        statistic_diff['position'] = newer_player_statistics.player.position
        statistic_diff['age'] = newer_player_statistics.age
        statistic_diff['strength'] = strength
        statistic_diff['name'] = '<a href="%s">%s</a>' % (newer_player_statistics.player.get_absolute_url(),
                                                          newer_player_statistics.player.name)
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
        statistic_diff['awp_to_next_bound'] = awp_to_next_bound

        return statistic_diff


@method_decorator(login_required, name='dispatch')
class PlayerDetailView(DetailView):
    context_object_name = 'player'
    template_name = 'core/ofm/player_detail.html'
    queryset = Player.objects.all()

    def get_context_data(self, **kwargs):
        context = super(PlayerDetailView, self).get_context_data(**kwargs)

        player = self.get_object()
        current_season = Matchday.objects.all()[0].season
        seasons = []
        player_stats = PlayerStatistics.objects.filter(player=player).order_by('matchday')
        for player_stat in player_stats:
            if player_stat.matchday.season not in seasons:
                seasons.append(player_stat.matchday.season)

        context['seasons'] = seasons
        if player:
            context['player_age'] = current_season.number - player.birth_season.number
            context['player_strength'] = player_stats[0].strength

        return context

    def get_object(self, **kwargs):
        player = super(PlayerDetailView, self).get_object()
        contracts = Contract.objects.filter(user=self.request.user, player=player, sold_on_matchday=None)
        return player if contracts.count() > 0 else None


@method_decorator(login_required, name='dispatch')
class PlayerChartView(CsrfExemptMixin, JsonRequestResponseMixin, View):
    def get(self, request):
        current_season_number = Matchday.objects.all()[0].season.number
        season_number = request.GET.get('season_number', default=current_season_number)
        player_id = request.GET.get('player_id')
        player = Player.objects.filter(id=player_id)
        player_statistics = PlayerStatistics.objects.filter(player=player, matchday__season__number=season_number)
        awps = [player_stat.awp for player_stat in player_statistics]

        chart_json = {
            "series": [{
                "name": 'AWP',
                "data": awps
            }],
            "categories": [player_stat.matchday.number for player_stat in player_statistics]
        }

        matchdays = [p.matchday for p in player_statistics]
        current_player_statistics = PlayerStatistics.objects.filter(player=player).order_by('matchday')[0]

        current_awp_boundaries = AwpBoundaries.get_from_matchday(current_player_statistics.matchday)

        for strength in current_awp_boundaries:
            if current_awp_boundaries[strength] >= min(awps) and strength > current_player_statistics.strength:
                awp_boundary_values = [AwpBoundaries.get_from_matchday(matchday)[strength] for matchday in matchdays]
                chart_json['series'].append({'name': 'AWP-Grenze: %s' % strength, 'data': awp_boundary_values})
            if current_awp_boundaries[strength] >= max(awps):
                break

        return self.render_json_response(chart_json)
