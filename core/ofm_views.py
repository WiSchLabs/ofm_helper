from core.models import Player, Contract
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, TemplateView


@method_decorator(login_required, name='dispatch')
class PlayerListView(ListView):
    context_object_name = 'player_list'
    template_name = 'core/ofm/player_list.html'

    def get_queryset(self):
        contracts = Contract.objects.filter(user=self.request.user, sold_on_matchday=None)
        return [contract.player for contract in contracts]


@method_decorator(login_required, name='dispatch')
class PlayerDataView(TemplateView):
    template_name = 'core/ofm/player_data.html'

    def get_context_data(self, **kwargs):
        contracts = Contract.objects.filter(user=self.request.user, sold_on_matchday=None)
        players = [contract.player for contract in contracts]
        player_statistics = [player.statistics.all() for player in players]

        return {'player_statistics': player_statistics}


@method_decorator(login_required, name='dispatch')
class PlayerDetailView(DetailView):
    context_object_name = 'player'
    template_name = 'core/ofm/player_detail.html'
    queryset = Player.objects.all()

    def get_object(self):
        player = super(PlayerDetailView, self).get_object()
        contracts = Contract.objects.filter(user=self.request.user, player=player, sold_on_matchday=None)
        return player if contracts.count() > 0 else None
