from braces.views import CsrfExemptMixin, JsonRequestResponseMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import TemplateView

from core.models import Matchday, Finance
from core.views.view_utils import validate_filtered_field


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
        newer_matchday_season = self.request.GET.get('newer_matchday_season',
                                                     default=Matchday.objects.all()[0].season.number)
        newer_matchday = self.request.GET.get('newer_matchday', default=Matchday.objects.all()[0].number)
        older_matchday_season = self.request.GET.get('older_matchday_season')
        older_matchday = self.request.GET.get('older_matchday')

        newer_finances = Finance.objects.filter(
            user=request.user,
            matchday__season__number=newer_matchday_season,
            matchday__number=newer_matchday
        )
        older_finances = Finance.objects.filter(
            user=request.user,
            matchday__season__number=older_matchday_season,
            matchday__number=older_matchday
        )

        newer_finances = validate_filtered_field(newer_finances)
        older_finances = validate_filtered_field(older_finances)

        finances_json = self._get_finances_diff_in_json(newer_finances, older_finances)

        return self.render_json_response(finances_json)

    @staticmethod
    def _get_finances_diff_in_json(newer_finances, older_finances):
        """
        Returns:
            A dictionary of finance data. If older_finances is None newer_finances is returned
        """

        if not newer_finances:
            newer_finances = Finance.objects.all().order_by('matchday')[0]

        account_balance = newer_finances.balance

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
            income_visitors_friendlies = newer_finances.income_visitors_friendlies - \
                                         older_finances.income_visitors_friendlies

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
            expenses_player_salaries = -(
                newer_finances.expenses_player_salaries - older_finances.expenses_player_salaries)

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

        for idx, _ in enumerate(data_source):
            if idx + 1 < data_source.count():
                income_visitors_league.append(
                    data_source[idx + 1].income_visitors_league - data_source[idx].income_visitors_league)
                income_sponsoring.append(data_source[idx + 1].income_sponsoring - data_source[idx].income_sponsoring)
                income_cup.append(data_source[idx + 1].income_cup - data_source[idx].income_cup)
                income_interests.append(data_source[idx + 1].income_interests - data_source[idx].income_interests)
                income_loan.append(data_source[idx + 1].income_loan - data_source[idx].income_loan)
                income_transfer.append(data_source[idx + 1].income_transfer - data_source[idx].income_transfer)
                income_visitors_friendlies.append(
                    data_source[idx + 1].income_visitors_friendlies - data_source[idx].income_visitors_friendlies)
                income_friendlies.append(data_source[idx + 1].income_friendlies - data_source[idx].income_friendlies)
                income_funcup.append(data_source[idx + 1].income_funcup - data_source[idx].income_funcup)
                income_betting.append(data_source[idx + 1].income_betting - data_source[idx].income_betting)
                matchdays.append(data_source[idx + 1].matchday.number)

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

        for idx, _ in enumerate(data_source):
            if idx + 1 < data_source.count():
                expenses_player_salaries.append(
                    data_source[idx].expenses_player_salaries - data_source[idx + 1].expenses_player_salaries)
                expenses_stadium.append(data_source[idx].expenses_stadium - data_source[idx + 1].expenses_stadium)
                expenses_youth.append(data_source[idx].expenses_youth - data_source[idx + 1].expenses_youth)
                expenses_interests.append(data_source[idx].expenses_interests - data_source[idx + 1].expenses_interests)
                expenses_trainings.append(data_source[idx].expenses_trainings - data_source[idx + 1].expenses_trainings)
                expenses_transfer.append(data_source[idx].expenses_transfer - data_source[idx + 1].expenses_transfer)
                expenses_compensation.append(
                    data_source[idx].expenses_compensation - data_source[idx + 1].expenses_compensation)
                expenses_friendlies.append(
                    data_source[idx].expenses_friendlies - data_source[idx + 1].expenses_friendlies)
                expenses_funcup.append(data_source[idx].expenses_funcup - data_source[idx + 1].expenses_funcup)
                expenses_betting.append(data_source[idx].expenses_betting - data_source[idx + 1].expenses_betting)
                matchdays.append(data_source[idx + 1].matchday.number)

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
