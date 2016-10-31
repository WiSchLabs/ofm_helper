import django
from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('core.urls'), name='core'),
]

if not settings.DEBUG:
    urlpatterns += [url(r'^static/(?P<path>.*)$', django.views.static.serve,
                        {'document_root': settings.STATIC_ROOT, 'show_indexes': settings.DEBUG})]
