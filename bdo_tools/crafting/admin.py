from django.contrib import admin

from . import models

admin.site.register(models.Material)
admin.site.register(models.Station)
admin.site.register(models.Recipe)
