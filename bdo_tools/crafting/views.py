from django.views.generic import ListView, TemplateView

from crafting import models


class MainView(TemplateView):
    template_name = 'crafting/main.html'


class MaterialListView(ListView):
    template_name = 'crafting/list.html'
    model = models.Material

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['model_name'] = 'Material'
        context['column_fields'] = ['name']
        context['detail_url_base'] = 'crafting:materials:detail'
        return context
