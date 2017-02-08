import numpy
from braces.views import CsrfExemptMixin
from braces.views import JsonRequestResponseMixin
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.cache import cache_page
from django.views.generic import TemplateView
from matplotlib import pyplot
from matplotlib import style
from matplotlib import ticker
from matplotlib.backends.backend_agg import FigureCanvas
from matplotlib.ticker import AutoMinorLocator

from core.managers.panda_manager import PandaManager, TransferFilter

style.use('ggplot')


@cache_page(60 * 60)
def render_plot(request):
    panda_manager = PandaManager()

    prices = panda_manager.get_grouped_prices('Strength', positions=['MS'], ages=[32], max_price=3 * 10 ** 7)

    fig = pyplot.figure(figsize=(16, 9), dpi=120)
    ax = fig.add_subplot(1, 1, 1)

    x = numpy.array(prices.mean().index)
    y = prices.mean()
    y_error = prices.std()

    pyplot.xticks(x)
    ax.yaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}'))
    ax.yaxis.set_minor_locator(AutoMinorLocator())
    ax.tick_params(which='both', direction='out', length=4, width=1)

    ax.grid(which='minor', alpha=0.4)
    ax.grid(which='major', alpha=0.7)

    pyplot.errorbar(x, y, yerr=y_error, fmt='o', color='g')
    pyplot.ylabel('Preis')
    pyplot.title('Spielerpreise')

    canvas = FigureCanvas(fig)
    response = HttpResponse(content_type='image/png')
    canvas.print_png(response)
    return response


@method_decorator(login_required, name='dispatch')
class TransfersChartView(CsrfExemptMixin, JsonRequestResponseMixin, View):
    def get(self, request):
        group_by = request.GET.get('group_by', default='Age')

        ages = request.GET.get('ages', default=None)
        strengths = request.GET.get('strengths', default=None)
        positions = request.GET.get('positions', default=None)
        seasons = request.GET.get('seasons', default=None)
        matchdays = request.GET.get('matchdays', default=None)
        min_price = request.GET.get('min_price', default=None)
        max_price = request.GET.get('max_price', default=None)

        if ages:
            ages = self._to_int_list(ages)
        if strengths:
            strengths = self._to_int_list(strengths)
        if positions:
            positions = self._to_list(positions)
        if seasons:
            seasons = self._to_int_list(seasons)
        if matchdays:
            matchdays = self._to_int_list(matchdays)
        if min_price:
            min_price = self._to_int(min_price)
        if max_price:
            max_price = self._to_int(max_price)

        panda_manager = PandaManager()
        prices = panda_manager.get_grouped_prices(group_by,
                                                  ages=ages,
                                                  strengths=strengths,
                                                  positions=positions,
                                                  seasons=seasons,
                                                  matchdays=matchdays,
                                                  min_price=min_price,
                                                  max_price=max_price,
                                                  )

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

        chart_json = {
            "series": [
                {
                    "name": 'Preise',
                    "data": data
                },
            ],
            "categories":
                list(map(int, numpy.array(prices.mean().index)))
        }

        return self.render_json_response(chart_json)

    @staticmethod
    def _to_int_list(l):
        return list(map(lambda x: int(x), l.split(',')))

    @staticmethod
    def _to_list(l):
        return l.split(',')

    @staticmethod
    def _to_int(l):
        return int(l)


@method_decorator(login_required, name='dispatch')
class TransfersView(TemplateView):
    template_name = 'core/ofm/transfers.html'