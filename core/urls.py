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
    url(r'^trigger_parsing/?$', views.trigger_parsing, name='trigger_parsing'),
    url(r'^logout/?$', views.logout_view, name='logout'),
    url(r'^ofm/', include('core.ofm_urls'), name='ofm'),
]
