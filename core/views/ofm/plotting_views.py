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

from core.managers.panda_manager import PandaManager

style.use('ggplot')


@cache_page(60 * 60)
def render_plot(request):
    panda_manager = PandaManager()

    prices = panda_manager.get_grouped_prices('Strength', positions=['MS'], ages=[17])

    fig = pyplot.figure(figsize=(16, 9), dpi=120)
    ax = fig.add_subplot(111)

    x = numpy.array(prices.mean().index)
    y = prices.mean()
    yerr = prices.std()

    ax.yaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}'))

    pyplot.errorbar(x, y, yerr=yerr, fmt='o')

    canvas = FigureCanvas(fig)
    response = HttpResponse(content_type='image/png')
    canvas.print_png(response)
    return response


@method_decorator(login_required, name='dispatch')
class TransfersView(TemplateView):
    template_name = 'core/ofm/transfers.html'
