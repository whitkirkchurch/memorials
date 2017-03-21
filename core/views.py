from django.views.generic import TemplateView, ListView, DetailView

from core import models

# Create your views here.


class HomeView(TemplateView):

    template_name = 'home.html'


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
