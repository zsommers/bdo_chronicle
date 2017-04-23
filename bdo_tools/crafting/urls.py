from django.conf.urls import include, url
from django.views.generic import DetailView, ListView, TemplateView

from . import models

materials_patterns = [
    url(r'^(?P<pk>[0-9]+)/$', DetailView.as_view(model=models.Material), name='detail'),
    url(r'^$', ListView.as_view(model=models.Material), name='list'),
]

recipes_patterns = [
    url(r'^(?P<pk>[0-9]+)/$', DetailView.as_view(model=models.Recipe), name='detail'),
    url(r'^$', ListView.as_view(model=models.Recipe), name='list'),
]

stations_patterns = [
    url(r'^(?P<pk>[0-9]+)/$', DetailView.as_view(model=models.Station), name='detail'),
    url(r'^$', ListView.as_view(model=models.Station), name='list'),
]

app_name = 'crafting'
urlpatterns = [
    url(r'^materials/', include(materials_patterns, namespace='materials')),
    url(r'^recipes/', include(recipes_patterns, namespace='recipes')),
    url(r'^stations/', include(stations_patterns, namespace='stations')),
    url(r'^$', TemplateView.as_view(template_name='crafting/main.html'), name='main'),
]
