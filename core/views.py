from django.shortcuts import render

from django.views.generic import TemplateView, ListView, DetailView

from django.core.paginator import Paginator

from . import models

# Create your views here.


class index(TemplateView):

    template_name = 'index.html'


class LocationListView(ListView):

    model = models.Location
    context_object_name = 'locations'


class LocationView(DetailView):

    model = models.Location
    context_object_name = 'location'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        memorials = context['location'].memorials.all()

        context['paginator'] = Paginator(memorials, 20)

        page = self.request.GET.get('page')
        context['memorials'] = context['paginator'].get_page(page)

        return context


class MemorialListView(ListView):

    model = models.Memorial
    paginate_by = 20
    context_object_name = 'memorials'


class MemorialView(DetailView):

    model = models.Memorial
    context_object_name = 'memorial'


class NameListView(ListView):

    model = models.Name
    paginate_by = 20
    context_object_name = 'names'
