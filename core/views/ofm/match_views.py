import locale

from braces.views import CsrfExemptMixin, JsonRequestResponseMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import TemplateView

from core.models import Matchday, Match


@method_decorator(login_required, name='dispatch')
class MatchesView(TemplateView):
    template_name = 'core/ofm/matches.html'

    def get_context_data(self, **kwargs):
        context = super(MatchesView, self).get_context_data(**kwargs)

        matchdays = Matchday.objects.filter(matches__isnull=False).distinct()
        seasons = set(m.season.number for m in matchdays)

        context['seasons'] = sorted(seasons, reverse=True)

        return context


@method_decorator(login_required, name='dispatch')
class MatchesAsJsonView(CsrfExemptMixin, JsonRequestResponseMixin, View):
    def get(self, request, *args, **kwargs):
        season = self.request.GET.get('season', default=Matchday.objects.all()[0].season.number)
        matches = Match.objects.filter(user=self.request.user, matchday__season__number=season)

        match_json = [self._get_match_in_json(match) for match in matches]

        return self.render_json_response(match_json)

    @staticmethod
    def _get_match_in_json(match):
        """
        Returns:
            A dictionary of match data.
        """
        locale.setlocale(locale.LC_ALL, '')

        guest_team_name, home_team_name = MatchesAsJsonView._get_formatted_team_names(match)
        venue = MatchesAsJsonView._get_formatted_venue(match)
        result = MatchesAsJsonView._get_formatted_score(match)
        guest_team_strength, home_team_strength = MatchesAsJsonView._get_formatted_team_strengths(match)

        match_stat = dict()
        match_stat['home_team'] = home_team_name
        match_stat['guest_team'] = guest_team_name
        match_stat['result'] = result
        match_stat['home_strength'] = home_team_strength
        match_stat['guest_strength'] = guest_team_strength
        match_stat['home_ball_possession'] = locale.format("%.1f", match.home_team_statistics.ball_possession) + " %"
        match_stat['guest_ball_possession'] = locale.format("%.1f", match.guest_team_statistics.ball_possession) + " %"
        match_stat['home_chances'] = match.home_team_statistics.chances
        match_stat['guest_chances'] = match.guest_team_statistics.chances
        match_stat['home_yellow_cards'] = match.home_team_statistics.yellow_cards
        match_stat['guest_yellow_cards'] = match.guest_team_statistics.yellow_cards
        match_stat['home_red_cards'] = match.home_team_statistics.red_cards
        match_stat['guest_red_cards'] = match.guest_team_statistics.red_cards
        match_stat['venue'] = venue
        match_stat['matchday'] = match.matchday.number

        return match_stat

    @staticmethod
    def _get_formatted_team_strengths(match):
        home_strength = match.home_team_statistics.strength
        guest_strength = match.guest_team_statistics.strength

        if home_strength == int(home_strength):
            home_team_strength = int(home_strength)
        else:
            home_team_strength = locale.format("%.1f", home_strength)
        if guest_strength == int(guest_strength):
            guest_team_strength = int(guest_strength)
        else:
            guest_team_strength = locale.format("%.1f", guest_strength)

        return guest_team_strength, home_team_strength

    @staticmethod
    def _get_formatted_team_names(match):
        if match.is_home_match:
            home_team_name = "<span class='users-team'>" + match.home_team_statistics.team_name + "</span>"
            guest_team_name = match.guest_team_statistics.team_name
        else:
            home_team_name = match.home_team_statistics.team_name
            guest_team_name = "<span class='users-team'>" + match.guest_team_statistics.team_name + "</span>"
        return guest_team_name, home_team_name

    @staticmethod
    def _get_formatted_venue(match):
        if match.is_home_match:
            if hasattr(match, 'stadium_statistics'):
                venue = "<a href='" + match.stadium_statistics.get_absolute_url() + "'>" + match.venue + "</a>"
            else:
                venue = match.venue
        else:
            venue = match.venue
        return venue

    @staticmethod
    def _get_formatted_score(match):
        result_score = str(match.home_team_statistics.score) + ":" + str(match.guest_team_statistics.score)
        if match.is_in_future:
            result = "<span class='match_scheduled alert-info'>-:-</span>"
        elif match.is_won:
            result = "<span class='match_won alert-success'>" + result_score + "</span>"
        elif match.is_draw:
            result = "<span class='match_draw alert-warning'>" + result_score + "</span>"
        else:
            result = "<span class='match_lost alert-danger'>" + result_score + "</span>"
        return result


@method_decorator(login_required, name='dispatch')
class MatchesSummaryJsonView(CsrfExemptMixin, JsonRequestResponseMixin, View):
    def get(self, request, *args, **kwargs):
        current_season = Matchday.objects.all()[0].season
        season_number = self.request.GET.get('season_number', current_season.number)
        matches_won = len(
            [match for match in Match.objects.filter(matchday__season__number=season_number) if match.is_won])
        matches_draw = len(
            [match for match in Match.objects.filter(matchday__season__number=season_number) if match.is_draw])
        matches_lost = len(
            [match for match in Match.objects.filter(matchday__season__number=season_number) if match.is_lost])

        json = {
            "matches_won": matches_won,
            "matches_draw": matches_draw,
            "matches_lost": matches_lost
        }

        return self.render_json_response(json)
