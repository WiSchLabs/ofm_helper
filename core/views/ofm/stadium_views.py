import ast
import locale

from braces.views import CsrfExemptMixin, JsonRequestResponseMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import TemplateView, DetailView

from core.models import Matchday, Match, MatchStadiumStatistics, StadiumStandStatistics

HTML_PERCENT_SIGN = " &#37;"

DEFAULT_SLIDER_MIN = 100
DEFAULT_SLIDER_MAX = 150
DEFAULT_TOLERANCE = 5
DEFAULT_HARMONIC_STRENGTH = 150


@method_decorator(login_required, name='dispatch')
class StadiumStatisticsView(TemplateView):
    template_name = 'core/ofm/stadium_statistics.html'

    def get_context_data(self, **kwargs):
        context = super(StadiumStatisticsView, self).get_context_data(**kwargs)

        self._add_seasons_to_context(context)
        self._add_slider_values_to_context(context)
        self._add_stadium_configurations_to_context(context)

        return context

    @staticmethod
    def _add_seasons_to_context(context):
        matchdays = Matchday.objects.filter(matches__isnull=False).distinct()
        seasons = set(m.season.number for m in matchdays)
        context['seasons'] = sorted(seasons, reverse=True)

    def _add_slider_values_to_context(self, context):
        slider_min, slider_max, tolerance = self._get_slider_values()
        context['slider_min'] = slider_min
        context['slider_max'] = slider_max
        context['tolerance'] = tolerance

    @staticmethod
    def _add_stadium_configurations_to_context(context):
        unique_stadium_configurations = []
        stadium_configurations = [s.get_configuration() for s in MatchStadiumStatistics.objects.all()]
        for s in stadium_configurations:
            if s not in unique_stadium_configurations:
                unique_stadium_configurations.append(s)
        context['stadium_configurations'] = reversed(unique_stadium_configurations)

    def _get_slider_values(self):
        slider_min = DEFAULT_SLIDER_MIN
        slider_max = DEFAULT_SLIDER_MAX
        tolerance = DEFAULT_TOLERANCE

        if Match.objects.count() > 0:
            slider_min, slider_max = self._get_strength_slider_values_from_last_match()

        if self.request.COOKIES.get('slider_min') \
                and self.request.COOKIES.get('slider_max') \
                and self.request.COOKIES.get('tolerance'):
            slider_min, slider_max, tolerance = self._get_slider_values_from_cookies()

        return slider_min, slider_max, tolerance

    def _get_strength_slider_values_from_last_match(self):
        match = Match.objects.filter(user=self.request.user, is_home_match=True).order_by('matchday')[0]
        slider_min = int(min(match.home_team_statistics.strength, match.guest_team_statistics.strength))
        slider_max = int(max(match.home_team_statistics.strength, match.guest_team_statistics.strength))
        return slider_min, slider_max

    def _get_slider_values_from_cookies(self):
        return (int(self.request.COOKIES['slider_min']),
                int(self.request.COOKIES['slider_max']),
                int(self.request.COOKIES['tolerance']))


@method_decorator(login_required, name='dispatch')
class StadiumStatisticsAsJsonView(CsrfExemptMixin, JsonRequestResponseMixin, View):
    def get(self, request, *args, **kwargs):

        harmonic_strength = self._get_harmonic_strength()
        tolerance = self._get_tolerance()

        matches = Match.objects.filter(user=self.request.user).order_by('matchday')
        filtered_matches = [match for match in matches if
                            harmonic_strength - tolerance <= match.harmonic_strength <= harmonic_strength + tolerance]

        stadium_statistics = []
        for match in filtered_matches:
            stat = MatchStadiumStatistics.objects.filter(match=match)
            if stat.count() > 0:
                stadium_statistics.append(stat[0])

        stadium_configuration_filter = self.request.GET.get('configuration_filter')
        filtered_stadium_stats = []
        if stadium_configuration_filter:
            for stat in stadium_statistics:
                if stat.get_configuration() == ast.literal_eval(stadium_configuration_filter):
                    filtered_stadium_stats.append(stat)
        else:
            filtered_stadium_stats = stadium_statistics

        stadium_statistics_json = [self._get_stadium_statistics_in_json(stat) for stat in filtered_stadium_stats]

        return self.render_json_response(stadium_statistics_json)

    def _get_harmonic_strength(self):
        harmonic_strength = DEFAULT_HARMONIC_STRENGTH
        if self.request.COOKIES.get('slider_min') and self.request.COOKIES.get('slider_max'):
            harmonic_strength = self._get_harmonic_strength_from_cookies()
        if self.request.GET.get('harmonic_strength'):
            harmonic_strength = int(self.request.GET['harmonic_strength'])
        return harmonic_strength

    def _get_tolerance(self):
        tolerance = DEFAULT_TOLERANCE
        if self.request.COOKIES.get('tolerance'):
            tolerance = self._get_tolerance_from_cookies()
        return tolerance

    def _get_harmonic_strength_from_cookies(self):
        slider_min = int(self.request.COOKIES['slider_min'])
        slider_max = int(self.request.COOKIES['slider_max'])
        return self._harmonic_strength(slider_min, slider_max)

    def _get_tolerance_from_cookies(self):
        if self.request.COOKIES.get('tolerance'):
            tolerance = int(self.request.COOKIES['tolerance'])
        return tolerance

    @staticmethod
    def _harmonic_strength(slider_min, slider_max):
        return round(2 * slider_min * slider_max / (slider_min + slider_max))

    @staticmethod
    def _get_stadium_statistics_in_json(stadium_stat):
        """
        Returns:
            A dictionary of stadium statistics data.
        """
        locale.setlocale(locale.LC_ALL, '')

        match_stadium_stat = dict()
        match_stadium_stat['season'] = stadium_stat.match.matchday.season.number
        match_stadium_stat['matchday'] = "<a href='" + stadium_stat.get_absolute_url() + "'>" + str(
            stadium_stat.match.matchday.number) + "</a>"
        if stadium_stat.visitors and stadium_stat.capacity:
            match_stadium_stat['visitors'] = stadium_stat.visitors
            match_stadium_stat['capacity'] = stadium_stat.capacity
            match_stadium_stat['earnings'] = stadium_stat.earnings
            match_stadium_stat['workload'] = locale.format("%.2f",
                                                           stadium_stat.visitors /
                                                           stadium_stat.capacity * 100) + HTML_PERCENT_SIGN
        else:
            # all stadium stands were under construction during match
            match_stadium_stat['visitors'] = 0
            match_stadium_stat['capacity'] = 0
            match_stadium_stat['earnings'] = 0
            match_stadium_stat['workload'] = 0
        match_stadium_stat['venue'] = stadium_stat.match.venue
        home_strength = stadium_stat.match.home_team_statistics.strength
        if home_strength == int(home_strength):
            match_stadium_stat['home_strength'] = int(home_strength)
        else:
            match_stadium_stat['home_strength'] = locale.format("%.1f", home_strength)
        guest_strength = stadium_stat.match.guest_team_statistics.strength
        if guest_strength == int(guest_strength):
            match_stadium_stat['guest_strength'] = int(guest_strength)
        else:
            match_stadium_stat['guest_strength'] = locale.format("%.1f", guest_strength)
        harmonic_strength = 2 * home_strength * guest_strength / (home_strength + guest_strength)
        match_stadium_stat['harmonic_strength'] = locale.format("%.1f", harmonic_strength)
        match_stadium_stat['light_level'] = str(stadium_stat.level.light.current_level) + " (" + str(
            stadium_stat.level.light.value) + " &euro;)   " + str(stadium_stat.level.light.daily_costs) + " &euro;"
        match_stadium_stat['screen_level'] = str(stadium_stat.level.screen.current_level) + " (" + str(
            stadium_stat.level.screen.value) + " &euro;)   " + str(stadium_stat.level.screen.daily_costs) + " &euro;"
        match_stadium_stat['security_level'] = str(stadium_stat.level.security.current_level) + " (" + str(
            stadium_stat.level.security.value) + " &euro;)   " + str(
            stadium_stat.level.security.daily_costs) + " &euro;"
        match_stadium_stat['parking_level'] = str(stadium_stat.level.parking.current_level) + " (" + str(
            stadium_stat.level.parking.value) + " &euro;)   " + str(stadium_stat.level.parking.daily_costs) + " &euro;"

        return match_stadium_stat


@method_decorator(login_required, name='dispatch')
class StadiumDetailView(DetailView):
    context_object_name = 'stadium_stat'
    template_name = 'core/ofm/stadium_detail.html'
    model = MatchStadiumStatistics

    def get_context_data(self, **kwargs):
        context = super(StadiumDetailView, self).get_context_data(**kwargs)

        if self.get_object():
            context['north_stand'] = self._get_stand_by_sector('N')
            context['south_stand'] = self._get_stand_by_sector('S')
            context['west_stand'] = self._get_stand_by_sector('W')
            context['east_stand'] = self._get_stand_by_sector('O')

        return context

    def get_object(self, **kwargs):
        stadium_stat = super(StadiumDetailView, self).get_object()
        matches = Match.objects.filter(user=self.request.user, stadium_statistics=stadium_stat)
        return stadium_stat if matches.count() > 0 else None

    def _get_stand_by_sector(self, sector):
        stand_statistics = StadiumStandStatistics.objects.filter(stadium_statistics=self.get_object(), sector=sector)
        return stand_statistics[0] if stand_statistics.count() > 0 else None


@method_decorator(login_required, name='dispatch')
class StadiumStandStatisticsView(TemplateView):
    template_name = 'core/ofm/stadium_stand_statistics.html'

    def get_context_data(self, **kwargs):
        context = super(StadiumStandStatisticsView, self).get_context_data(**kwargs)

        current_season_number = Matchday.objects.all()[0].season.number
        sector = self.request.GET.get('sector', 'N')
        season_number = self.request.GET.get('season', current_season_number)
        queryset = StadiumStandStatistics.objects.filter(
            stadium_statistics__match__user=self.request.user,
            stadium_statistics__match__matchday__season__number=season_number,
            sector=sector
        )

        seasons = []
        sectors = []
        statistics = StadiumStandStatistics.objects.filter(
            stadium_statistics__match__user=self.request.user
        ).order_by('stadium_statistics__match__matchday')
        for stat in statistics:
            if stat.stadium_statistics.match.matchday.season not in seasons:
                seasons.append(stat.stadium_statistics.match.matchday.season)
            if stat.get_sector() not in sectors:
                sectors.append(stat.get_sector())

        context['seasons'] = seasons
        context['sectors'] = sectors

        context['sector'] = sector
        context['season'] = season_number
        if queryset.count() > 0:
            context['sector_name'] = queryset[0].get_sector()

        return context


@method_decorator(login_required, name='dispatch')
class StadiumStandStatisticsChartView(CsrfExemptMixin, JsonRequestResponseMixin, View):
    def get(self, request, *args, **kwargs):
        current_season_number = Matchday.objects.all()[0].season.number
        season_number = self.request.GET.get('season_number', default=current_season_number)
        sector = self.request.GET.get('sector', 'N')
        statistics = StadiumStandStatistics.objects.filter(
            stadium_statistics__match__user=self.request.user,
            stadium_statistics__match__matchday__season__number=season_number,
            sector=sector
        )

        chart_json = {
            "series": [{
                "name": 'Kapazität',
                "data": [s.level.capacity for s in statistics],
                "yAxis": 0
            }, {
                "name": 'Zuschauer',
                "data": [s.visitors for s in statistics],
                "yAxis": 0
            }, {
                "name": 'Ticketpreis',
                "data": [s.ticket_price for s in statistics],
                "yAxis": 1
            }, {
                "name": 'Zustand',
                "data": [float(s.condition) for s in statistics],
                "yAxis": 1
            }, {
                "name": 'Gemittelte Stärke der Mannschaften',
                "data": [float("{0:.2f}".format(s.stadium_statistics.match.harmonic_strength)) for s in statistics],
                "yAxis": 1
            }],
            "categories": [s.stadium_statistics.match.matchday.number for s in statistics],
            "yAxis": [{
                "title": {
                    "text": 'Kapazität & Zuschauer'
                },
                'min': 0
            }, {
                "title": {
                    "text": 'Ticketpreis, Zustand & Stärke'
                },
                'min': 0,
                "opposite": "true"
            }]
        }

        return self.render_json_response(chart_json)
