from braces.views import CsrfExemptMixin, JsonRequestResponseMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import View

from core.models import Matchday


@method_decorator(login_required, name='dispatch')
class GetCurrentMatchdayView(CsrfExemptMixin, JsonRequestResponseMixin, View):
    def get(self, request):
        current_matchday = Matchday.get_current()
        matchday_json = dict()
        matchday_json['matchday_number'] = current_matchday.number
        matchday_json['season_number'] = current_matchday.season.number
        return self.render_json_response(matchday_json)
