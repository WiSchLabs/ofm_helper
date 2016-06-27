from django.conf.urls import url

from core import views

app_name = 'ofm'
urlpatterns = [
    url(r'^player_statistics/?$', views.test_chart_view, name='player_statistics'),
]
