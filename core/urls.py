from django.conf.urls import include, url
from django.views.generic.base import RedirectView, TemplateView

import core.views.account_views
import core.views.settings_views
import core.views.trigger_parsing_views

app_name = 'core'
urlpatterns = [
    url(r'^favicon\.ico$', RedirectView.as_view(url='/static/core/img/OFM_favicon.png', permanent=True)),
    url(r'^$', TemplateView.as_view(template_name='core/home.html'), name='home'),

    url(r'^register/?$', core.views.account_views.register_view, name='register'),
    url(r'^login/?$', core.views.account_views.login_view, name='login'),
    url(r'^account/?$', core.views.account_views.account_view, name='account'),
    url(r'^logout/?$', core.views.account_views.logout_view, name='logout'),

    url(r'^ofm/', include('core.ofm_urls'), name='ofm'),
    url(r'^checklist/', include('core.checklist_urls'), name='checklist'),

    url(r'^settings/?$', core.views.settings_views.settings_view,
        name='settings'),

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
