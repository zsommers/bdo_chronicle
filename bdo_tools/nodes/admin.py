from django import forms
from django.contrib import admin
from django.core.urlresolvers import reverse
import nested_admin

from . import models


#
# Forms
#
class ConnectedNodeForm(forms.ModelForm):
    class Meta:
        model = models.Node
        fields = ['name', 'territory', 'is_hub', 'contribution_cost',
                  'node_manager', 'connected_nodes']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        qs = models.Node.objects.exclude(id__exact=self.instance.id)
        self.fields['connected_nodes'].queryset = qs


#
# Inlines
#
class ResourceInline(admin.TabularInline):
    model = models.Resource
    extra = 0  # Don't show any rows by default


class NestedPropertyStationInline(nested_admin.NestedTabularInline):
    model = models.PropertyStation
    # Always show 3 rows, but don't show extra blanks beyond that
    extra = 0
    min_num = 3


class PropertyInline(nested_admin.NestedTabularInline):
    model = models.Property
    extra = 0
    raw_id_fields = ()
    inlines = [NestedPropertyStationInline]


class PropertyStationInline(admin.TabularInline):
    model = models.PropertyStation
    # Always show 3 rows, but don't show extra blanks beyond that
    extra = 0
    min_num = 3


#
# Admins
#
class TerritoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'kingdom')
    list_filter = ('kingdom',)
    search_fields = ('name',)
    ordering = ('name',)


class NodeAdmin(nested_admin.NestedModelAdmin):
    # List options
    list_display = ('name', 'is_hub', 'territory', 'get_kingdom')
    list_filter = ('territory', 'is_hub')
    search_fields = ('name',)
    ordering = ('name',)
    form = ConnectedNodeForm

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
    inlines = [ResourceInline, PropertyInline]


class ResourceAdmin(admin.ModelAdmin):
    list_display = ('node', 'material', 'contribution_cost')
    list_filter = ('node', 'material', 'contribution_cost')


class PropertyAdmin(admin.ModelAdmin):
    inlines = [PropertyStationInline]

#
# Admin Setup
#
admin.site.register(models.Kingdom)
admin.site.register(models.Territory, TerritoryAdmin)
admin.site.register(models.Node, NodeAdmin)
admin.site.register(models.Resource, ResourceAdmin)
admin.site.register(models.Property, PropertyAdmin)