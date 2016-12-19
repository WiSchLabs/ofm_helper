from django.conf.urls import url

import core.views.account_views
import core.views.settings_views
import core.views.trigger_parsing_views

from core.views.account_views import OFMUserCreate

app_name = 'account'
urlpatterns = [
    url(r'^register/?$', OFMUserCreate.as_view(), name='register'),
    url(r'^login/?$', core.views.account_views.login_view, name='login'),
    url(r'^$', core.views.account_views.account_view, name='home'),
    url(r'^logout/?$', core.views.account_views.logout_view, name='logout'),
    url(r'^settings/?$', core.views.settings_views.settings_view, name='settings'),
]
