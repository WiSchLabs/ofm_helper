from django.conf.urls import url
from django.views.generic.base import TemplateView

app_name = 'core'
urlpatterns = [
    # url(r'^favicon\.ico$', RedirectView.as_view(url='/static/autostew_web_home/img/Logo_RGB.png', permanent=True)),
    url(r'^$', TemplateView.as_view(template_name='core/home.html'), name='home'),
]