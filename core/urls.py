from core import views
from django.conf.urls import url, include
from django.views.generic.base import TemplateView, RedirectView

app_name = 'core'
urlpatterns = [
    url(r'^favicon\.ico$', RedirectView.as_view(url='/static/core/img/OFM_favicon.png', permanent=True)),
    url(r'^$', TemplateView.as_view(template_name='core/home.html'), name='home'),
    url(r'^register/?$', views.register_view, name='register'),
    url(r'^login/?$', views.login_view, name='login'),
    url(r'^account/?$', views.account_view, name='account'),
    url(r'^logout/?$', views.logout_view, name='logout'),
    url(r'^ofm/', include('core.ofm_urls'), name='ofm'),

    url(r'^trigger_parsing/?$', views.trigger_parsing, name='trigger_parsing'),
    url(r'^trigger_matchday_parsing/?$', views.trigger_matchday_parsing, name='trigger_matchday_parsing'),
    url(r'^trigger_players_parsing/?$', views.trigger_players_parsing, name='trigger_players_parsing'),
    url(r'^trigger_player_statistics_parsing/?$', views.trigger_player_statistics_parsing, name='trigger_player_statistics_parsing'),
    url(r'^trigger_finances_parsing/?$', views.trigger_finances_parsing, name='trigger_finances_parsing'),
    url(r'^trigger_match_parsing/?$', views.trigger_match_parsing, name='trigger_match_parsing'),
]
