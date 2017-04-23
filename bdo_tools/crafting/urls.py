from django.conf.urls import include, url
from django.views.generic import DetailView, ListView

from . import models, views

materials_patterns = [
    url(r'^(?P<pk>[0-9]+)/$', DetailView.as_view(model=models.Material), name='detail'),
    url(r'^$', ListView.as_view(model=models.Material), name='list'),
]

app_name = 'crafting'
urlpatterns = [
    url(r'^materials/', include(materials_patterns, namespace='materials')),
    url(r'^$', views.MainView.as_view(), name='main'),
]
