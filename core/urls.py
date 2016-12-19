from django.conf.urls import include, url
from django.views.generic.base import RedirectView, TemplateView

app_name = 'core'
urlpatterns = [
    url(r'^favicon\.ico$', RedirectView.as_view(url='/static/core/img/OFM_favicon.png', permanent=True)),
    url(r'^$', TemplateView.as_view(template_name='core/home.html'), name='home'),

    url(r'^ofm/', include('core.ofm_urls'), name='ofm'),
    url(r'^checklist/', include('core.checklist_urls'), name='checklist'),
    url(r'^trigger/', include('core.trigger_parsing_urls'), name='trigger'),
    url(r'^account/', include('core.account_urls'), name='account'),
]
