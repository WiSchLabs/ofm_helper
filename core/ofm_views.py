from core.models import Player, PlayerUserOwnership
from django.views.generic import ListView, DetailView


class PlayerListView(ListView):
    context_object_name = 'player_list'
    template_name = 'core/ofm/player_list.html'

    def get_queryset(self):
        contracts = PlayerUserOwnership.objects.filter(user=self.request.user, sold_on_matchday=None)
        return [contract.player for contract in contracts]


class PlayerDetailView(DetailView):
    context_object_name = 'player'
    template_name = 'core/ofm/player_detail.html'
    queryset = Player.objects.all()

    def get_object(self):
        player = super(PlayerDetailView, self).get_object()
        contracts = PlayerUserOwnership.objects.filter(user=self.request.user, player=player, sold_on_matchday=None)
        return player if contracts.count() > 0 else None
