import numpy
from braces.views import CsrfExemptMixin
from braces.views import JsonRequestResponseMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import TemplateView

from core.managers.panda_manager import PandaManager, TransferFilter


@method_decorator(login_required, name='dispatch')
class TransfersDetailChartView(CsrfExemptMixin, JsonRequestResponseMixin, View):

    def get(self, request):
        group_by = request.GET.get('group_by', default='Strength')

        ages = _to_int_list(request.GET.get('ages', default=None))
        strengths = _to_int_list(request.GET.get('strengths', default=None))
        positions = _to_list(request.GET.get('positions', default=None))
        seasons = _to_int_list(request.GET.get('seasons', default=None))
        matchdays = _to_int_list(request.GET.get('matchdays', default=None))
        min_price = _to_int(request.GET.get('min_price', default=None))
        max_price = _to_int(request.GET.get('max_price', default=None))

        if positions == 'All':
            positions = None

        panda_manager = PandaManager()

        ungrouped_dataframe = panda_manager.filter_transfers(TransferFilter(ages=ages,
                                                                            strengths=strengths,
                                                                            positions=positions,
                                                                            seasons=seasons,
                                                                            matchdays=matchdays,
                                                                            min_price=min_price,
                                                                            max_price=max_price,))

        prices = panda_manager.get_grouped_prices(group_by,
                                                  ages=ages,
                                                  strengths=strengths,
                                                  positions=positions,
                                                  seasons=seasons,
                                                  matchdays=matchdays,
                                                  min_price=min_price,
                                                  max_price=max_price,
                                                  )

        chart_json = {
            "series": [
                {
                    "name": 'Preise',
                    "data": self._get_data_from_dataframe(prices)
                },
            ],
            "categories": self.convert_to_json_serializable_list(prices),
            "ages": list(map(int, list(ungrouped_dataframe.groupby('Age').Age.nunique().index))),
            "strengths": list(map(int, list(ungrouped_dataframe.groupby('Strength').Strength.nunique().index))),
            "positions": list(ungrouped_dataframe.groupby('Position').Position.nunique().index),
            "seasons": list(map(int, list(ungrouped_dataframe.groupby('Season').Season.nunique().index))),
            "matchdays": list(map(int, list(ungrouped_dataframe.groupby('Matchday').Matchday.nunique().index))),
        }

        return self.render_json_response(chart_json)

    @staticmethod
    def convert_to_json_serializable_list(prices):
        try:
            int(numpy.array(prices.mean().index[0]))
            return list(map(int, numpy.array(prices.mean().index)))
        except TypeError:
            return list(map(str, numpy.array(prices.mean().index)))

    @staticmethod
    def _get_data_from_dataframe(prices):
        mins = prices.min()
        quantiles = prices.quantile([0.25, 0.75])
        medians = prices.median()
        maxs = prices.max()
        data = []
        for x_index in numpy.array(prices.mean().index):
            data.append([float(mins[x_index]),
                         float(quantiles[x_index][0.25]),
                         float(medians[x_index]),
                         float(quantiles[x_index][0.75]),
                         float(maxs[x_index])
                         ])
        return data


@method_decorator(login_required, name='dispatch')
class TransfersOverviewTableView(CsrfExemptMixin, JsonRequestResponseMixin, View):

    def get(self, request):
        group_by = _to_list(request.GET.get('group_by', default='Strength,Age'))

        ages = _to_int_list(request.GET.get('ages', default=None))
        strengths = _to_int_list(request.GET.get('strengths', default=None))
        positions = _to_list(request.GET.get('positions', default=None))
        if positions == 'All':
            positions = None

        panda_manager = PandaManager()

        prices = panda_manager.get_grouped_prices(group_by,
                                                  ages=ages,
                                                  strengths=strengths,
                                                  positions=positions,
                                                  seasons=_to_int_list(request.GET.get('seasons', default=None)),
                                                  matchdays=_to_int_list(request.GET.get('matchdays', default=None)),
                                                  min_price=_to_int(request.GET.get('min_price', default=None)),
                                                  max_price=_to_int(request.GET.get('max_price', default=None)),
                                                  )

        strengths = list(set(map(lambda x: x[0], prices.groups)))
        ages = list(set(map(lambda x: x[1], prices.groups)))
        ages.sort()
        strengths.sort()

        table_json = dict()

        table_json['ages'] = ages
        table_json['strengths'] = strengths
        table_json['medians'] = self._get_medians(ages, prices, strengths)

        return self.render_json_response(table_json)

    @staticmethod
    def _get_medians(ages, prices, strengths):
        medians = []
        for age in ages:
            row = []
            for strength in strengths:
                try:
                    row.append(prices.get_group((strength, age)).median())
                except KeyError:
                    row.append('NA')
            medians.append(row)
        return medians


@method_decorator(login_required, name='dispatch')
class TransfersView(TemplateView):
    template_name = 'core/ofm/transfers.html'


def _to_int_list(l):
    if l:
        return list(map(int, l.split(',')))
    return None


def _to_list(l):
    if l:
        return l.split(',')
    return None


def _to_int(l):
    if l:
        return int(l)
    return None
