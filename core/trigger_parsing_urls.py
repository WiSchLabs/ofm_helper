from django.conf.urls import url
import core.views.trigger_parsing_views

app_name = 'trigger'
urlpatterns = [
    url(r'^trigger_parsing/?$', core.views.trigger_parsing_views.trigger_parsing,
        name='trigger_parsing'),
    url(r'^trigger_matchday_parsing/?$', core.views.trigger_parsing_views.trigger_matchday_parsing,
        name='trigger_matchday_parsing'),
    url(r'^trigger_players_parsing/?$', core.views.trigger_parsing_views.trigger_players_parsing,
        name='trigger_players_parsing'),
    url(r'^trigger_player_statistics_parsing/?$', core.views.trigger_parsing_views.trigger_player_statistics_parsing,
        name='trigger_player_statistics_parsing'),
    url(r'^trigger_finances_parsing/?$', core.views.trigger_parsing_views.trigger_finances_parsing,
        name='trigger_finances_parsing'),
    url(r'^trigger_match_parsing/?$', core.views.trigger_parsing_views.trigger_match_parsing,
        name='trigger_match_parsing'),
]
