from braces.views import CsrfExemptMixin, JsonRequestResponseMixin
from chartit import DataPool, Chart
from core.models import Player, Contract, PlayerStatistics, Finance, Matchday, Match, MatchStadiumStatistics, \
    StadiumStandStatistics
from django.contrib.auth.decorators import login_required
from django.core.exceptions import MultipleObjectsReturned
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, TemplateView, View


def _validate_filtered_field(field):
        if len(field) > 1:
            raise MultipleObjectsReturned
        elif field:
            field = field[0]
        return field


@method_decorator(login_required, name='dispatch')
class PlayerStatisticsView(TemplateView):
    template_name = 'core/ofm/player_statistics.html'

    def get_context_data(self, **kwargs):
        matchdays = Matchday.objects.filter(player_statistics__isnull=False).distinct()

        context = super(PlayerStatisticsView, self).get_context_data(**kwargs)
        context['matchdays'] = matchdays

        return context


@method_decorator(login_required, name='dispatch')
class PlayerStatisticsAsJsonView(CsrfExemptMixin, JsonRequestResponseMixin, View):

    def get(self, request, *args, **kwargs):
        contracts = Contract.objects.filter(user=self.request.user, sold_on_matchday=None)
        players = [contract.player for contract in contracts]

        newer_matchday_season = self.request.GET.get('newer_matchday_season', default=Matchday.objects.all()[0].season.number)
        newer_matchday = self.request.GET.get('newer_matchday', default=Matchday.objects.all()[0].number)
        older_matchday_season = self.request.GET.get('older_matchday_season')
        older_matchday = self.request.GET.get('older_matchday')

        player_statistics_tuples = []
        for player in players:
            newer_player_statistic, older_player_statistic = self._get_statistics_from_player_and_matchday(player,
                                                                            newer_matchday_season, newer_matchday,
                                                                            older_matchday_season, older_matchday)
            if not (not older_player_statistic and (older_matchday and older_matchday_season)) \
                    and not (not newer_player_statistic and (newer_matchday and newer_matchday_season)):
                player_statistics_tuples.append((newer_player_statistic, older_player_statistic))
            else:
                pass

        player_statistics_json = [self._get_player_statistics_diff_in_json(newer_player_statistic, older_player_statistic)
                                  for (newer_player_statistic, older_player_statistic) in player_statistics_tuples]

        return self.render_json_response(player_statistics_json)

    def _get_statistics_from_player_and_matchday(self, player,
                                                 newer_matchday_season, newer_matchday,
                                                 older_matchday_season, older_matchday):

        ps1 = PlayerStatistics.objects.filter(player=player, matchday__season__number=newer_matchday_season, matchday__number=newer_matchday)
        ps2 = PlayerStatistics.objects.filter(player=player, matchday__season__number=older_matchday_season, matchday__number=older_matchday)

        ps1 = _validate_filtered_field(ps1)
        ps2 = _validate_filtered_field(ps2)

        return ps1, ps2

    def _get_player_statistics_diff_in_json(self, newer_player_statistics, older_player_statistics):
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
        current_season = Matchday.objects.all()[0].season
        seasons = []
        player_stats = PlayerStatistics.objects.filter(player=player).order_by('matchday')
        for player_stat in player_stats:
            if player_stat.matchday.season not in seasons:
                seasons.append(player_stat.matchday.season)

        context['seasons'] = seasons
        if player:
            context['player_age'] = current_season.number - player.birth_season.number

        return context

    def get_object(self, **kwargs):
        player = super(PlayerDetailView, self).get_object()
        contracts = Contract.objects.filter(user=self.request.user, player=player, sold_on_matchday=None)
        return player if contracts.count() > 0 else None


@method_decorator(login_required, name='dispatch')
class PlayerChartView(CsrfExemptMixin, JsonRequestResponseMixin, View):

    def get(self, request, *args, **kwargs):
        current_season_number = Matchday.objects.all()[0].season.number
        season_number = self.request.GET.get('season_number', default=current_season_number)
        player_id = self.request.GET.get('player_id')
        player = Player.objects.filter(id=player_id)
        data_source = PlayerStatistics.objects.filter(player=player, matchday__season__number=season_number)

        chart_json = {
            "series": [{
                "name": 'AWP',
                "data": [player_stat.awp for player_stat in data_source]
            }],
            "categories": [player_stat.matchday.number for player_stat in data_source]
        }

        return self.render_json_response(chart_json)


@method_decorator(login_required, name='dispatch')
class FinanceDataView(TemplateView):
    template_name = 'core/ofm/finances.html'

    def get_context_data(self, **kwargs):
        context = super(FinanceDataView, self).get_context_data(**kwargs)
        matchdays = Matchday.objects.filter(finance__isnull=False).distinct()
        context['matchdays'] = matchdays

        return context


@method_decorator(login_required, name='dispatch')
class FinancesAsJsonView(CsrfExemptMixin, JsonRequestResponseMixin, View):

    def get(self, request, *args, **kwargs):
        newer_matchday_season = self.request.GET.get('newer_matchday_season', default=Matchday.objects.all()[0].season.number)
        newer_matchday = self.request.GET.get('newer_matchday', default=Matchday.objects.all()[0].number)
        older_matchday_season = self.request.GET.get('older_matchday_season')
        older_matchday = self.request.GET.get('older_matchday')

        newer_finances = Finance.objects.filter(user=request.user, matchday__season__number=newer_matchday_season, matchday__number=newer_matchday)
        older_finances = Finance.objects.filter(user=request.user, matchday__season__number=older_matchday_season, matchday__number=older_matchday)

        newer_finances = _validate_filtered_field(newer_finances)
        older_finances = _validate_filtered_field(older_finances)

        finances_json = self._get_finances_diff_in_json(newer_finances, older_finances)

        return self.render_json_response(finances_json)

    def _get_finances_diff_in_json(self, newer_finances, older_finances):
        """
        Args:
            newer_finances: newer finances
            older_finances: older finances

        Returns:
            A dictionary of finance data. If older_finances is None newer_finances is returned
        """

        if not newer_finances:
            newer_finances = Finance.objects.all()[0]

        account_balance = newer_finances.balance
        balance = newer_finances.balance
        if older_finances:
            balance = newer_finances.balance - older_finances.balance

        income_visitors_league = newer_finances.income_visitors_league
        if older_finances:
            income_visitors_league = newer_finances.income_visitors_league - older_finances.income_visitors_league

        income_sponsoring = newer_finances.income_sponsoring
        if older_finances:
            income_sponsoring = newer_finances.income_sponsoring - older_finances.income_sponsoring
            
        income_cup = newer_finances.income_cup
        if older_finances:
            income_cup = newer_finances.income_cup - older_finances.income_cup

        income_interests = newer_finances.income_interests
        if older_finances:
            income_interests = newer_finances.income_interests - older_finances.income_interests
            
        income_loan = newer_finances.income_loan
        if older_finances:
            income_loan = newer_finances.income_loan - older_finances.income_loan
            
        income_transfer = newer_finances.income_transfer
        if older_finances:
            income_transfer = newer_finances.income_transfer - older_finances.income_transfer
            
        income_visitors_friendlies = newer_finances.income_visitors_friendlies
        if older_finances:
            income_visitors_friendlies = newer_finances.income_visitors_friendlies - older_finances.income_visitors_friendlies
            
        income_friendlies = newer_finances.income_friendlies
        if older_finances:
            income_friendlies = newer_finances.income_friendlies - older_finances.income_friendlies
            
        income_funcup = newer_finances.income_funcup
        if older_finances:
            income_funcup = newer_finances.income_funcup - older_finances.income_funcup
            
        income_betting = newer_finances.income_betting
        if older_finances:
            income_betting = newer_finances.income_betting - older_finances.income_betting
            
        expenses_player_salaries = -newer_finances.expenses_player_salaries
        if older_finances:
            expenses_player_salaries = -(newer_finances.expenses_player_salaries - older_finances.expenses_player_salaries)
            
        expenses_stadium = -newer_finances.expenses_stadium
        if older_finances:
            expenses_stadium = -(newer_finances.expenses_stadium - older_finances.expenses_stadium)
            
        expenses_youth = -newer_finances.expenses_youth
        if older_finances:
            expenses_youth = -(newer_finances.expenses_youth - older_finances.expenses_youth)
            
        expenses_interests = -newer_finances.expenses_interests
        if older_finances:
            expenses_interests = -(newer_finances.expenses_interests - older_finances.expenses_interests)
            
        expenses_trainings = -newer_finances.expenses_trainings
        if older_finances:
            expenses_trainings = -(newer_finances.expenses_trainings - older_finances.expenses_trainings)
            
        expenses_transfer = -newer_finances.expenses_transfer
        if older_finances:
            expenses_transfer = -(newer_finances.expenses_transfer - older_finances.expenses_transfer)
            
        expenses_compensation = -newer_finances.expenses_compensation
        if older_finances:
            expenses_compensation = -(newer_finances.expenses_compensation - older_finances.expenses_compensation)
            
        expenses_friendlies = -newer_finances.expenses_friendlies
        if older_finances:
            expenses_friendlies = -(newer_finances.expenses_friendlies - older_finances.expenses_friendlies)
            
        expenses_funcup = -newer_finances.expenses_funcup
        if older_finances:
            expenses_funcup = -(newer_finances.expenses_funcup - older_finances.expenses_funcup)
            
        expenses_betting = -newer_finances.expenses_betting
        if older_finances:
            expenses_betting = -(newer_finances.expenses_betting - older_finances.expenses_betting)

        finances_diff = dict()
        finances_diff['account_balance'] = account_balance

        finances_diff['income_visitors_league'] = income_visitors_league
        finances_diff['income_sponsoring'] = income_sponsoring
        finances_diff['income_cup'] = income_cup
        finances_diff['income_interests'] = income_interests
        finances_diff['income_loan'] = income_loan
        finances_diff['income_transfer'] = income_transfer
        finances_diff['income_visitors_friendlies'] = income_visitors_friendlies
        finances_diff['income_friendlies'] = income_friendlies
        finances_diff['income_funcup'] = income_funcup
        finances_diff['income_betting'] = income_betting

        finances_diff['expenses_player_salaries'] = expenses_player_salaries
        finances_diff['expenses_stadium'] = expenses_stadium
        finances_diff['expenses_youth'] = expenses_youth
        finances_diff['expenses_interests'] = expenses_interests
        finances_diff['expenses_trainings'] = expenses_trainings
        finances_diff['expenses_transfer'] = expenses_transfer
        finances_diff['expenses_compensation'] = expenses_compensation
        finances_diff['expenses_friendlies'] = expenses_friendlies
        finances_diff['expenses_funcup'] = expenses_funcup
        finances_diff['expenses_betting'] = expenses_betting

        sum_income = income_visitors_league + income_sponsoring + income_cup + income_interests + income_loan + \
                     income_transfer + income_visitors_friendlies + income_friendlies + income_funcup + income_betting
        sum_expenses = expenses_player_salaries + expenses_stadium + expenses_youth + expenses_interests + \
                       expenses_trainings + expenses_transfer + expenses_compensation + expenses_friendlies + \
                       expenses_funcup + expenses_betting

        finances_diff['sum_income'] = sum_income
        finances_diff['sum_expenses'] = sum_expenses
        finances_diff['balance'] = sum_income + sum_expenses

        return [finances_diff]


@method_decorator(login_required, name='dispatch')
class FinanceBalanceChartView(CsrfExemptMixin, JsonRequestResponseMixin, View):

    def get(self, request, *args, **kwargs):
        current_season_number = Matchday.objects.all()[0].season.number
        season_number = self.request.GET.get('season_number', default=current_season_number)
        data_source = Finance.objects.filter(user=self.request.user, matchday__season__number=season_number)

        chart_json = {
            "series": [{
                "name": 'Kontostand',
                "data": [finance.balance for finance in data_source]
            }],
            "categories": [finance.matchday.number for finance in data_source]
        }

        return self.render_json_response(chart_json)


@method_decorator(login_required, name='dispatch')
class FinanceIncomeChartView(CsrfExemptMixin, JsonRequestResponseMixin, View):

    def get(self, request, *args, **kwargs):
        current_season_number = Matchday.objects.all()[0].season.number
        season_number = self.request.GET.get('season_number', default=current_season_number)
        data_source = Finance.objects.filter(user=self.request.user, matchday__season__number=season_number)

        income_visitors_league = []
        income_sponsoring = []
        income_cup = []
        income_interests = []
        income_loan = []
        income_transfer = []
        income_visitors_friendlies = []
        income_friendlies = []
        income_funcup = []
        income_betting = []
        matchdays = []

        if len(data_source) >= 1:
            income_visitors_league.append(data_source[0].income_visitors_league)
            income_sponsoring.append(data_source[0].income_sponsoring)
            income_cup.append(data_source[0].income_cup)
            income_interests.append(data_source[0].income_interests)
            income_loan.append(data_source[0].income_loan)
            income_transfer.append(data_source[0].income_transfer)
            income_visitors_friendlies.append(data_source[0].income_visitors_friendlies)
            income_friendlies.append(data_source[0].income_friendlies)
            income_funcup.append(data_source[0].income_funcup)
            income_betting.append(data_source[0].income_betting)
            matchdays.append(data_source[0].matchday.number)

        for idx, entry in enumerate(data_source):
            if idx+1 < data_source.count():
                income_visitors_league.append(data_source[idx+1].income_visitors_league - data_source[idx].income_visitors_league)
                income_sponsoring.append(data_source[idx+1].income_sponsoring - data_source[idx].income_sponsoring)
                income_cup.append(data_source[idx+1].income_cup - data_source[idx].income_cup)
                income_interests.append(data_source[idx+1].income_interests - data_source[idx].income_interests)
                income_loan.append(data_source[idx+1].income_loan - data_source[idx].income_loan)
                income_transfer.append(data_source[idx+1].income_transfer - data_source[idx].income_transfer)
                income_visitors_friendlies.append(data_source[idx+1].income_visitors_friendlies - data_source[idx].income_visitors_friendlies)
                income_friendlies.append(data_source[idx+1].income_friendlies - data_source[idx].income_friendlies)
                income_funcup.append(data_source[idx+1].income_funcup - data_source[idx].income_funcup)
                income_betting.append(data_source[idx+1].income_betting - data_source[idx].income_betting)
                matchdays.append(data_source[idx+1].matchday.number)

        series = []
        if sum(income_visitors_league) is not 0:
            series.append({"name": 'Ticketeinnahmen Liga', "data": income_visitors_league})
        if sum(income_sponsoring) is not 0:
            series.append({"name": 'Sponsor', "data": income_sponsoring})
        if sum(income_cup) is not 0:
            series.append({"name": 'Pokal', "data": income_cup})
        if sum(income_interests) is not 0:
            series.append({"name": 'Zinsen', "data": income_interests})
        if sum(income_loan) is not 0:
            series.append({"name": 'Kredite', "data": income_loan})
        if sum(income_transfer) is not 0:
            series.append({"name": 'Spielertransfers', "data": income_transfer})
        if sum(income_visitors_friendlies) is not 0:
            series.append({"name": 'Ticketeinnahmen Freundschaftsspiele', "data": income_visitors_friendlies})
        if sum(income_friendlies) is not 0:
            series.append({"name": 'Freundschaftsspiele', "data": income_friendlies})
        if sum(income_funcup) is not 0:
            series.append({"name": 'Fun-Cup', "data": income_funcup})
        if sum(income_betting) is not 0:
            series.append({"name": 'Wetten', "data": income_betting})

        chart_json = {
            "series": series,
            "categories": matchdays
        }

        return self.render_json_response(chart_json)


@method_decorator(login_required, name='dispatch')
class FinanceExpensesChartView(CsrfExemptMixin, JsonRequestResponseMixin, View):

    def get(self, request, *args, **kwargs):
        current_season_number = Matchday.objects.all()[0].season.number
        season_number = self.request.GET.get('season_number', default=current_season_number)
        data_source = Finance.objects.filter(user=self.request.user, matchday__season__number=season_number)

        expenses_player_salaries = []
        expenses_stadium = []
        expenses_youth = []
        expenses_interests = []
        expenses_trainings = []
        expenses_transfer = []
        expenses_compensation = []
        expenses_friendlies = []
        expenses_funcup = []
        expenses_betting = []
        matchdays = []

        if len(data_source) >= 1:
            expenses_player_salaries.append(-data_source[0].expenses_player_salaries)
            expenses_stadium.append(-data_source[0].expenses_stadium)
            expenses_youth.append(-data_source[0].expenses_youth)
            expenses_interests.append(-data_source[0].expenses_interests)
            expenses_trainings.append(-data_source[0].expenses_trainings)
            expenses_transfer.append(-data_source[0].expenses_transfer)
            expenses_compensation.append(-data_source[0].expenses_compensation)
            expenses_friendlies.append(-data_source[0].expenses_friendlies)
            expenses_funcup.append(-data_source[0].expenses_funcup)
            expenses_betting.append(-data_source[0].expenses_betting)
            matchdays.append(data_source[0].matchday.number)

        for idx, entry in enumerate(data_source):
            if idx+1 < data_source.count():
                expenses_player_salaries.append(data_source[idx].expenses_player_salaries - data_source[idx+1].expenses_player_salaries)
                expenses_stadium.append(data_source[idx].expenses_stadium - data_source[idx+1].expenses_stadium)
                expenses_youth.append(data_source[idx].expenses_youth - data_source[idx+1].expenses_youth)
                expenses_interests.append(data_source[idx].expenses_interests - data_source[idx+1].expenses_interests)
                expenses_trainings.append(data_source[idx].expenses_trainings - data_source[idx+1].expenses_trainings)
                expenses_transfer.append(data_source[idx].expenses_transfer - data_source[idx+1].expenses_transfer)
                expenses_compensation.append(data_source[idx].expenses_compensation - data_source[idx+1].expenses_compensation)
                expenses_friendlies.append(data_source[idx].expenses_friendlies - data_source[idx+1].expenses_friendlies)
                expenses_funcup.append(data_source[idx].expenses_funcup - data_source[idx+1].expenses_funcup)
                expenses_betting.append(data_source[idx].expenses_betting - data_source[idx+1].expenses_betting)
                matchdays.append(data_source[idx+1].matchday.number)

        series = []
        if sum(expenses_player_salaries) is not 0:
            series.append({"name": 'Spielergehalt', "data": expenses_player_salaries})
        if sum(expenses_stadium) is not 0:
            series.append({"name": 'Stadion', "data": expenses_stadium})
        if sum(expenses_youth) is not 0:
            series.append({"name": u'Jugendförderung', "data": expenses_youth})
        if sum(expenses_interests) is not 0:
            series.append({"name": 'Zinsen', "data": expenses_interests})
        if sum(expenses_trainings) is not 0:
            series.append({"name": 'Training', "data": expenses_trainings})
        if sum(expenses_transfer) is not 0:
            series.append({"name": 'Spielertransfers', "data": expenses_transfer})
        if sum(expenses_compensation) is not 0:
            series.append({"name": 'Abfindungen', "data": expenses_compensation})
        if sum(expenses_friendlies) is not 0:
            series.append({"name": 'Freundschaftsspiele', "data": expenses_friendlies})
        if sum(expenses_funcup) is not 0:
            series.append({"name": 'Fun-Cup', "data": expenses_funcup})
        if sum(expenses_betting) is not 0:
            series.append({"name": 'Wetten', "data": expenses_betting})

        chart_json = {
            "series": series,
            "categories": matchdays
        }

        return self.render_json_response(chart_json)


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

    def _get_match_in_json(self, match):
        """
        Args:
            match: Match

        Returns:
            A dictionary of match data.
        """

        if match.is_home_match:
            home_team_name = "<span class='users-team'>" + match.home_team_statistics.team_name + "</span>"
            guest_team_name = match.guest_team_statistics.team_name
            if hasattr(match, 'stadium_statistics'):
                venue = "<a href='" + match.stadium_statistics.get_absolute_url() + "'>" + match.venue + "</a>"
            else:
                venue = match.venue
        else:
            home_team_name = match.home_team_statistics.team_name
            guest_team_name = "<span class='users-team'>" + match.guest_team_statistics.team_name + "</span>"
            venue = match.venue

        result_score = str(match.home_team_statistics.score) + ":" + str(match.guest_team_statistics.score)
        if match.is_won:
            result = "<span class='match_won alert-success'>" + result_score + "</span>"
        elif match.is_draw:
            result = "<span class='match_draw alert-warning'>" + result_score + "</span>"
        else:
            result = "<span class='match_lost alert-danger'>" + result_score + "</span>"

        match_stat = dict()
        match_stat['home_team'] = home_team_name
        match_stat['guest_team'] = guest_team_name
        match_stat['result'] = result
        match_stat['home_strength'] = match.home_team_statistics.strength
        match_stat['guest_strength'] = match.guest_team_statistics.strength
        match_stat['home_ball_possession'] = str(match.home_team_statistics.ball_possession) + " %"
        match_stat['guest_ball_possession'] = str(match.guest_team_statistics.ball_possession) + " %"
        match_stat['home_chances'] = match.home_team_statistics.chances
        match_stat['guest_chances'] = match.guest_team_statistics.chances
        match_stat['home_yellow_cards'] = match.home_team_statistics.yellow_cards
        match_stat['guest_yellow_cards'] = match.guest_team_statistics.yellow_cards
        match_stat['home_red_cards'] = match.home_team_statistics.red_cards
        match_stat['guest_red_cards'] = match.guest_team_statistics.red_cards
        match_stat['venue'] = venue
        match_stat['matchday'] = match.matchday.number

        return match_stat


@method_decorator(login_required, name='dispatch')
class StadiumStatisticsView(TemplateView):
    template_name = 'core/ofm/stadium_statistics.html'

    def get_context_data(self, **kwargs):
        context = super(StadiumStatisticsView, self).get_context_data(**kwargs)

        matchdays = Matchday.objects.filter(matches__isnull=False).distinct()
        seasons = set(m.season.number for m in matchdays)

        tolerance = 5
        if self.request.COOKIES.get('slider_min') and self.request.COOKIES.get('slider_max') and self.request.COOKIES.get('tolerance'):
            slider_min = self.request.COOKIES['slider_min']
            slider_max = self.request.COOKIES['slider_max']
            tolerance = self.request.COOKIES['tolerance']
        elif Match.objects.count() > 0:
            match = Match.objects.filter(user=self.request.user, is_home_match=True).order_by('matchday')[0]  # latest home match
            slider_min = min(match.home_team_statistics.strength, match.guest_team_statistics.strength)
            slider_max = max(match.home_team_statistics.strength, match.guest_team_statistics.strength)
        else:
            slider_min = 100
            slider_max = 150

        context['seasons'] = sorted(seasons, reverse=True)
        context['slider_min'] = slider_min
        context['slider_max'] = slider_max
        context['tolerance'] = tolerance

        return context


@method_decorator(login_required, name='dispatch')
class StadiumStatisticsAsJsonView(CsrfExemptMixin, JsonRequestResponseMixin, View):

    def get(self, request, *args, **kwargs):
        harmonic_strength = 150
        tolerance = 5
        if self.request.COOKIES.get('slider_min') and self.request.COOKIES.get('slider_max') and self.request.COOKIES.get('tolerance'):
            slider_min = int(self.request.COOKIES['slider_min'])
            slider_max = int(self.request.COOKIES['slider_max'])
            tolerance = int(self.request.COOKIES['tolerance'])
            harmonic_strength = round(2 * slider_min * slider_max / (slider_min + slider_max))
        harmonic_strength = self.request.GET.get('harmonic_strength', default=harmonic_strength)
        tolerance = self.request.GET.get('tolerance', default=tolerance)

        try:
            harmonic_strength = int(harmonic_strength)
            tolerance = int(tolerance)
        except TypeError:
            pass

        matches = Match.objects.filter(user=self.request.user).order_by('matchday')
        filtered_matches = [match for match in matches if
                            match.harmonic_strength <= harmonic_strength + tolerance and
                            match.harmonic_strength >= harmonic_strength - tolerance]

        stadium_statistics = []
        for match in filtered_matches:
            stat = MatchStadiumStatistics.objects.filter(match=match)
            if stat.count() > 0:
                stadium_statistics.append(stat[0])

        stadium_statistics_json = [self._get_stadium_statistics_in_json(stat) for stat in stadium_statistics]

        return self.render_json_response(stadium_statistics_json)

    def _get_stadium_statistics_in_json(self, stadium_stat):
        """
        Args:
            stadium_stat: MatchStadiumStatistics

        Returns:
            A dictionary of stadium statistics data.
        """

        match_stadium_stat = dict()
        match_stadium_stat['season'] = stadium_stat.match.matchday.season.number
        match_stadium_stat['matchday'] = "<a href='" + stadium_stat.get_absolute_url() + "'>" + str(stadium_stat.match.matchday.number) + "</a>"
        if stadium_stat.visitors and stadium_stat.capacity:
            match_stadium_stat['visitors'] = stadium_stat.visitors
            match_stadium_stat['capacity'] = stadium_stat.capacity
            match_stadium_stat['earnings'] = stadium_stat.earnings
            match_stadium_stat['workload'] = '{:.2f}'.format(stadium_stat.visitors / stadium_stat.capacity * 100) + " &#37;"
        else:
            # all stadium stands were under construction during match
            match_stadium_stat['visitors'] = 0
            match_stadium_stat['capacity'] = 0
            match_stadium_stat['earnings'] = 0
            match_stadium_stat['workload'] = 0
        match_stadium_stat['venue'] = stadium_stat.match.venue
        match_stadium_stat['home_strength'] = stadium_stat.match.home_team_statistics.strength
        match_stadium_stat['guest_strength'] = stadium_stat.match.guest_team_statistics.strength
        match_stadium_stat['harmonic_strength'] = 2*match_stadium_stat['home_strength']*match_stadium_stat['guest_strength']/(match_stadium_stat['home_strength']+match_stadium_stat['guest_strength'])
        match_stadium_stat['light_level'] = str(stadium_stat.level.light.current_level) + " (" + str(stadium_stat.level.light.value) + " &euro;)   " + str(stadium_stat.level.light.daily_costs) + " &euro;"
        match_stadium_stat['screen_level'] = str(stadium_stat.level.screen.current_level) + " (" + str(stadium_stat.level.screen.value) + " &euro;)   " + str(stadium_stat.level.screen.daily_costs) + " &euro;"
        match_stadium_stat['security_level'] = str(stadium_stat.level.security.current_level) + " (" + str(stadium_stat.level.security.value) + " &euro;)   " + str(stadium_stat.level.security.daily_costs) + " &euro;"
        match_stadium_stat['parking_level'] = str(stadium_stat.level.parking.current_level) + " (" + str(stadium_stat.level.parking.value) + " &euro;)   " + str(stadium_stat.level.parking.daily_costs) + " &euro;"

        return match_stadium_stat


@method_decorator(login_required, name='dispatch')
class StadiumDetailView(DetailView):
    context_object_name = 'stadium_stat'
    template_name = 'core/ofm/stadium_detail.html'
    queryset = MatchStadiumStatistics.objects.all()

    def get_context_data(self, **kwargs):
        context = super(StadiumDetailView, self).get_context_data(**kwargs)

        if self.get_object():
            north_stand = StadiumStandStatistics.objects.filter(stadium_statistics=self.get_object(), sector='N')
            south_stand = StadiumStandStatistics.objects.filter(stadium_statistics=self.get_object(), sector='S')
            west_stand = StadiumStandStatistics.objects.filter(stadium_statistics=self.get_object(), sector='W')
            east_stand = StadiumStandStatistics.objects.filter(stadium_statistics=self.get_object(), sector='O')

            context['north_stand'] = north_stand[0] if north_stand.count() > 0 else None
            context['south_stand'] = south_stand[0] if south_stand.count() > 0 else None
            context['west_stand'] = west_stand[0] if west_stand.count() > 0 else None
            context['east_stand'] = east_stand[0] if east_stand.count() > 0 else None

        return context

    def get_object(self, **kwargs):
        stadium_stat = super(StadiumDetailView, self).get_object()
        matches = Match.objects.filter(user=self.request.user, stadium_statistics=stadium_stat)
        return stadium_stat if matches.count() > 0 else None


@method_decorator(login_required, name='dispatch')
class StadiumStandStatisticsView(TemplateView):
    template_name = 'core/ofm/stadium_stand_statistics.html'

    def get_context_data(self, **kwargs):
        context = super(StadiumStandStatisticsView, self).get_context_data(**kwargs)

        current_season = Matchday.objects.all()[0].season
        sector = self.request.GET.get('sector', 'N')
        season_number = self.request.GET.get('season', current_season.number)
        queryset = StadiumStandStatistics.objects.filter(stadium_statistics__match__user=self.request.user,
                                                         stadium_statistics__match__matchday__season__number=season_number,
                                                         sector=sector)

        context['season'] = season_number
        if queryset.count() > 0:
            context['sector_name'] = queryset[0].get_sector()

        chart_data = DataPool(
            series=[{
                'options': {
                    'source': queryset
                },
                'terms': {
                    'Spieltag': 'stadium_statistics__match__matchday__number',
                    'Kapazität': 'level__capacity',
                    'Besucher': 'visitors',
                    'Ticketpreis': 'ticket_price',
                    'Zustand': 'condition'
                }
            }]
        )

        chart = Chart(
            datasource=chart_data,
            series_options=[{
                'options': {
                    'type': 'spline',
                    'xAxis': 0,
                    'yAxis': 0,
                    'zIndex': 1,
                    'stacking': False
                },
                'terms': {'Spieltag': ['Kapazität', 'Besucher', ]}
            }, {
                'options': {
                    'type': 'line',
                    'xAxis': 1,
                    'yAxis': 1,
                    'stacking': False
                },
                'terms': {'Spieltag': ['Ticketpreis', 'Zustand', ]}
            }],
            chart_options={
                'title': {
                    'text': 'Tribünenstatistik'
                },
                'yAxis': {
                    'min': 0
                },
            },
        )

        context['chart'] = chart

        return context
