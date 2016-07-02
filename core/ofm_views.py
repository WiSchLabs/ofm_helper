from core.models import Player
from django.views.generic import ListView, DetailView


class PlayerListView(ListView):
    model = Player
    template_name = 'core/ofm/player_list.html'


class PlayerDetailView(DetailView):
    model = Player
    template_name = 'core/ofm/player_detail.html'
