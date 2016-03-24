from django.contrib import admin
from django.core.urlresolvers import reverse

from . import models


class TerritoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'kingdom')
    list_filter = ('kingdom',)
    search_fields = ('name',)
    ordering = ('name',)


class ResourceInline(admin.TabularInline):
    model = models.Resource
    extra = 0  # Don't show any rows by default


class NodeAdmin(admin.ModelAdmin):
    # List options
    list_display = ('name', 'is_hub', 'territory', 'get_kingdom')
    list_filter = ('territory', 'is_hub')
    search_fields = ('name',)
    ordering = ('name',)

    def get_kingdom(self, obj):
        return obj.territory.kingdom.name
    get_kingdom.short_description = 'Kingdom'
    get_kingdom.admin_order_field = 'territory__kingdom__name'

    # Detail Options
    filter_horizontal = ('connected_nodes',)
    fieldsets = [
        (None, {'fields': ['name', 'territory', 'is_hub']}),
        ('Claiming', {'fields': ['contribution_cost', 'node_manager', 'connected_nodes']})
    ]
    inlines = [ResourceInline]


class ResourceAdmin(admin.ModelAdmin):
    list_display = ('node', 'material', 'contribution_cost')
    list_filter = ('node', 'material', 'contribution_cost')


class PropertyStationInline(admin.TabularInline):
    model = models.PropertyStation
    extra = 0
    min_num = 3


class PropertyAdmin(admin.ModelAdmin):
    inlines = [PropertyStationInline]


admin.site.register(models.Kingdom)
admin.site.register(models.Territory, TerritoryAdmin)
admin.site.register(models.Node, NodeAdmin)
admin.site.register(models.Resource, ResourceAdmin)
admin.site.register(models.Property, PropertyAdmin)