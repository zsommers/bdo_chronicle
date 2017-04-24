from django.conf.urls import include, url
from django.views.generic import DetailView, ListView, TemplateView

from . import models

kingdoms_patterns = [
    url(r'^(?P<pk>[0-9]+)/$', DetailView.as_view(model=models.Kingdom), name='detail'),
    url(r'^$', ListView.as_view(model=models.Kingdom), name='list'),
]

app_name = 'nodes'
urlpatterns = [
    url(r'^kingdoms/', include(kingdoms_patterns, namespace='kingdoms')),
    #  url(r'^recipes/', include(recipes_patterns, namespace='recipes')),
    #  url(r'^stations/', include(stations_patterns, namespace='stations')),
    url(r'^$', TemplateView.as_view(template_name='nodes/main.html'), name='main'),
]
