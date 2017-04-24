from django.conf.urls import include, url
from django.views.generic import DetailView, ListView, TemplateView

from . import models

kingdoms_patterns = [
    url(r'^(?P<pk>[0-9]+)/$', DetailView.as_view(model=models.Kingdom), name='detail'),
    url(r'^$', ListView.as_view(model=models.Kingdom), name='list'),
]

territories_patterns = [
    url(r'^(?P<pk>[0-9]+)/$', DetailView.as_view(model=models.Territory), name='detail'),
    url(r'^$', ListView.as_view(model=models.Territory), name='list'),
]

app_name = 'nodes'
urlpatterns = [
    url(r'^kingdoms/', include(kingdoms_patterns, namespace='kingdoms')),
    url(r'^territories/', include(territories_patterns, namespace='territories')),
    url(r'^$', TemplateView.as_view(template_name='nodes/main.html'), name='main'),
]
