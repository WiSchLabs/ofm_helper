from braces.views import CsrfExemptMixin, JsonRequestResponseMixin
from braces.views import JSONResponseMixin
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
class FinancesAsJsonView(CsrfExemptMixin, JSONResponseMixin, View):
    def get(self, request):
        newer_matchday_season = request.GET.get('newer_matchday_season',
                                                     default=Matchday.objects.all()[0].season.number)
        newer_matchday = request.GET.get('newer_matchday', default=Matchday.objects.all()[0].number)
        older_matchday_season = request.GET.get('older_matchday_season')
        older_matchday = request.GET.get('older_matchday')

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

        finances_diff = newer_finances.diff(Finance())
        if older_finances:
            finances_diff = newer_finances.diff(older_finances)

        finances_diff_dict = dict(finances_diff)

        finances_diff_dict['account_balance'] = newer_finances.balance
        finances_diff_dict['sum_income'] = finances_diff.income()
        finances_diff_dict['sum_expenses'] = finances_diff.expenses()
        finances_diff_dict['balance'] = finances_diff_dict['sum_income'] + finances_diff_dict['sum_expenses']

        return [finances_diff_dict]


@method_decorator(login_required, name='dispatch')
class FinanceBalanceChartView(CsrfExemptMixin, JsonRequestResponseMixin, View):
    def get(self, request):
        current_season_number = Matchday.objects.all()[0].season.number
        season_number = request.GET.get('season_number', default=current_season_number)
        data_source = Finance.objects.filter(user=request.user, matchday__season__number=season_number)

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
    def get(self, request):
        chart_json = _get_chart_json(request, self.create_income_series)
        return self.render_json_response(chart_json)

    @staticmethod
    def create_income_series(diffs):
        income_visitors_league = [diff.income_visitors_league for diff in diffs]
        income_sponsoring = [diff.income_sponsoring for diff in diffs]
        income_cup = [diff.income_cup for diff in diffs]
        income_interests = [diff.income_interests for diff in diffs]
        income_loan = [diff.income_loan for diff in diffs]
        income_transfer = [diff.income_transfer for diff in diffs]
        income_visitors_friendlies = [diff.income_visitors_friendlies for diff in diffs]
        income_friendlies = [diff.income_friendlies for diff in diffs]
        income_funcup = [diff.income_funcup for diff in diffs]
        income_betting = [diff.income_betting for diff in diffs]

        series = [_get_finance_attribute_json('Ticketeinnahmen Liga', income_visitors_league),
                  _get_finance_attribute_json('Sponsor', income_sponsoring),
                  _get_finance_attribute_json('Pokal', income_cup),
                  _get_finance_attribute_json('Zinsen', income_interests),
                  _get_finance_attribute_json('Kredite', income_loan),
                  _get_finance_attribute_json('Spielertransfers', income_transfer),
                  _get_finance_attribute_json('Ticketeinnahmen Freundschaftsspiele', income_visitors_friendlies),
                  _get_finance_attribute_json('Freundschaftsspiele', income_friendlies),
                  _get_finance_attribute_json('Fun-Cup', income_funcup),
                  _get_finance_attribute_json('Wetten', income_betting)]
        return series


@method_decorator(login_required, name='dispatch')
class FinanceExpensesChartView(CsrfExemptMixin, JsonRequestResponseMixin, View):
    def get(self, request):
        chart_json = _get_chart_json(request, self.create_expenses_series)
        return self.render_json_response(chart_json)

    @staticmethod
    def create_expenses_series(diffs):
        expenses_player_salaries = [diff.expenses_player_salaries for diff in diffs]
        expenses_stadium = [diff.expenses_stadium for diff in diffs]
        expenses_youth = [diff.expenses_youth for diff in diffs]
        expenses_interests = [diff.expenses_interests for diff in diffs]
        expenses_trainings = [diff.expenses_trainings for diff in diffs]
        expenses_transfer = [diff.expenses_transfer for diff in diffs]
        expenses_compensation = [diff.expenses_compensation for diff in diffs]
        expenses_friendlies = [diff.expenses_friendlies for diff in diffs]
        expenses_funcup = [diff.expenses_funcup for diff in diffs]
        expenses_betting = [diff.expenses_betting for diff in diffs]

        series = [_get_finance_attribute_json('Spielergehalt', expenses_player_salaries),
                  _get_finance_attribute_json('Stadion', expenses_stadium),
                  _get_finance_attribute_json(u'Jugendförderung', expenses_youth),
                  _get_finance_attribute_json('Zinsen', expenses_interests),
                  _get_finance_attribute_json('Training', expenses_trainings),
                  _get_finance_attribute_json('Spielertransfers', expenses_transfer),
                  _get_finance_attribute_json('Abfindungen', expenses_compensation),
                  _get_finance_attribute_json('Freundschaftsspiele', expenses_friendlies),
                  _get_finance_attribute_json('Fun-Cup', expenses_funcup),
                  _get_finance_attribute_json('Wetten', expenses_betting)]
        return series


def _get_chart_json(request, finance_method):
    current_season_number = Matchday.objects.all()[0].season.number
    season_number = request.GET.get('season_number', default=current_season_number)
    finances_this_season = Finance.objects.filter(user=request.user, matchday__season__number=season_number)
    diffs = []
    matchdays = []
    if len(finances_this_season) >= 1:
        first_finance_diff = finances_this_season[0].diff(Finance())

        diffs.append(first_finance_diff)
        matchdays.append(finances_this_season[0].matchday.number)
    for idx, _ in enumerate(finances_this_season):
        if idx + 1 < finances_this_season.count():
            diffs.append(finances_this_season[idx].diff(finances_this_season[idx + 1]))
            matchdays.append(finances_this_season[idx + 1].matchday.number)
    series = finance_method(diffs)
    chart_json = {
        "series": series,
        "categories": matchdays
    }
    return chart_json


def _get_finance_attribute_json(name, finance_data):
    if sum(finance_data) is not 0:
        return {"name": name, "data": finance_data}
    return {}
