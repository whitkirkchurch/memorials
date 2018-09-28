from django.shortcuts import render

from django.views.generic import TemplateView, ListView, DetailView

from . import models

# Create your views here.


class index(TemplateView):

    template_name = 'index.html'


class LocationListView(ListView):

    model = models.Location
    context_object_name = 'locations'


class MemorialListView(ListView):

    model = models.Memorial
    context_object_name = 'memorials'


class MemorialView(DetailView):

    model = models.Memorial
    context_object_name = 'memorial'


class NameListView(ListView):

    model = models.Name
    context_object_name = 'names'
