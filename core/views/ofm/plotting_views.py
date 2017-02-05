import matplotlib.ticker as mtick
import numpy
from django.http import HttpResponse
from django.views.decorators.cache import cache_page
from matplotlib import pyplot
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

from core.managers.panda_manager import PandaManager


@cache_page(60 * 60)
def render_plot(request):
    panda_manager = PandaManager()

    prices = panda_manager.get_prices_grouped_by_age()

    fig = pyplot.figure(figsize=(16, 9), dpi=120)
    ax = fig.add_subplot(111)

    x = numpy.array(prices.mean().index)
    y = prices.mean()
    yerr = prices.std()

    ax.yaxis.set_major_formatter(mtick.StrMethodFormatter('{x:,.0f}'))

    pyplot.errorbar(x, y, yerr=yerr, fmt='o')

    canvas = FigureCanvas(fig)
    response = HttpResponse(content_type='image/png')
    canvas.print_png(response)
    return response
