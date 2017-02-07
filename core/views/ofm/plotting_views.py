import numpy
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import TemplateView
from matplotlib import pyplot
from matplotlib import style
from matplotlib import ticker
from matplotlib.backends.backend_agg import FigureCanvas
from matplotlib.ticker import MultipleLocator

from core.managers.panda_manager import PandaManager

style.use('ggplot')


@cache_page(60 * 60)
def render_plot(request):
    panda_manager = PandaManager()

    prices = panda_manager.get_grouped_prices('Strength', positions=['MS'], ages=[32], max_price=3*10**7)

    fig = pyplot.figure(figsize=(16, 9), dpi=120)
    ax = fig.add_subplot(1, 1, 1)

    x = numpy.array(prices.mean().index)
    y = prices.mean()
    y_error = prices.std()

    ax.xaxis.set_major_locator(MultipleLocator(1))
    ax.yaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}'))
    ax.yaxis.set_minor_locator(MultipleLocator(_get_biggest_power_which_is_smaller_than_max_data(prices)))
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


def _get_biggest_power_which_is_smaller_than_max_data(prices):
    max_price = prices.mean().max()
    i = 0
    while 10 ** i < max_price:
        i += 1
    return 10 ** (i-2)


@method_decorator(login_required, name='dispatch')
class TransfersView(TemplateView):
    template_name = 'core/ofm/transfers.html'
