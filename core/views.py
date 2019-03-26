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

    def get_context_data(self,**kwargs):
        context = super(LocationListView,self).get_context_data(**kwargs)

        for location in context['locations']:
            location.memorial_count = location.memorials.filter(published=True).count()

        return context


class LocationView(DetailView):

    model = models.Location
    context_object_name = 'location'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        memorials = context['location'].memorials.filter(published=True)

        context['paginator'] = Paginator(memorials, 20)

        page = self.request.GET.get('page')
        context['memorials'] = context['paginator'].get_page(page)

        return context


class TagListView(ListView):

    model = models.Tag
    context_object_name = 'tags'


class TagView(DetailView):

    model = models.Tag
    context_object_name = 'tag'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        memorials = context['tag'].memorials.filter(published=True)

        context['paginator'] = Paginator(memorials, 20)

        page = self.request.GET.get('page')
        context['memorials'] = context['paginator'].get_page(page)

        return context


class MemorialListView(ListView):

    model = models.Memorial
    paginate_by = 20
    context_object_name = 'memorials'

    def get_queryset(self):
        return models.Memorial.objects.filter(published=True)


class MemorialView(DetailView):

    model = models.Memorial
    context_object_name = 'memorial'


class NameListView(ListView):

    model = models.Name
    paginate_by = 20
    context_object_name = 'names'
