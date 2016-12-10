from django.conf.urls import url, include
from django.views.generic.base import TemplateView, RedirectView

import core.views.account_views
import core.views.settings_views
import core.views.trigger_parsing_views
from core.views.base_views import GetCurrentMatchdayView
from core.views.checklist_views import GetChecklistItemsView, GetChecklistItemsForTodayView, CreateChecklistItemView, \
    UpdateChecklistPriorityView, UpdateChecklistItemView, DeleteChecklistItemView

app_name = 'core'
urlpatterns = [
    url(r'^favicon\.ico$', RedirectView.as_view(url='/static/core/img/OFM_favicon.png', permanent=True)),
    url(r'^$', TemplateView.as_view(template_name='core/home.html'), name='home'),
    url(r'^register/?$', core.views.account_views.register_view, name='register'),
    url(r'^login/?$', core.views.account_views.login_view, name='login'),
    url(r'^account/?$', core.views.account_views.account_view, name='account'),
    url(r'^logout/?$', core.views.account_views.logout_view, name='logout'),
    url(r'^ofm/', include('core.ofm_urls'), name='ofm'),
    url(r'^get_current_matchday/?$', GetCurrentMatchdayView.as_view(), name='get_current_matchday'),

    url(r'^settings/?$', core.views.settings_views.settings_view, name='settings'),
    url(r'^settings_get_checklist_items/?$', GetChecklistItemsView.as_view(), name='settings_get_checklist_items'),
    url(r'^settings_get_checklist_items_for_today/?$', GetChecklistItemsForTodayView.as_view(),
        name='settings_get_checklist_items_for_today'),
    url(r'^settings_add_checklist_item/?$', CreateChecklistItemView.as_view(), name='settings_add_checklist_item'),
    url(r'^settings_update_checklist_item/?$', UpdateChecklistItemView.as_view(),
        name='settings_update_checklist_item'),
    url(r'^settings_delete_checklist_item/?$', DeleteChecklistItemView.as_view(),
        name='settings_delete_checklist_item'),
    url(r'^settings_update_checklist_priority/?$', UpdateChecklistPriorityView.as_view(),
        name='settings_update_checklist_priority'),

    url(r'^trigger_parsing/?$', core.views.trigger_parsing_views.trigger_parsing, name='trigger_parsing'),
    url(r'^trigger_matchday_parsing/?$', core.views.trigger_parsing_views.trigger_matchday_parsing, name='trigger_matchday_parsing'),
    url(r'^trigger_players_parsing/?$', core.views.trigger_parsing_views.trigger_players_parsing, name='trigger_players_parsing'),
    url(r'^trigger_player_statistics_parsing/?$', core.views.trigger_parsing_views.trigger_player_statistics_parsing,
        name='trigger_player_statistics_parsing'),
    url(r'^trigger_finances_parsing/?$', core.views.trigger_parsing_views.trigger_finances_parsing, name='trigger_finances_parsing'),
    url(r'^trigger_match_parsing/?$', core.views.trigger_parsing_views.trigger_match_parsing, name='trigger_match_parsing'),
]
