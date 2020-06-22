from django.views.generic import TemplateView, ListView, DetailView

from django.core.paginator import Paginator

from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse

from . import models

# Create your views here.


class index(TemplateView):

    template_name = 'index.html'


class about(TemplateView):

    template_name = 'about.html'


class Disclaimer(TemplateView):

    template_name = 'disclaimer.html'


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

    def get_context_data(self,**kwargs):
        context = super(TagListView,self).get_context_data(**kwargs)

        for tag in context['tags']:
            tag.memorial_count = tag.memorials.filter(published=True).count()

        return context


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
    paginate_by = 50
    context_object_name = 'memorials'

    def get_queryset(self):
        return models.Memorial.objects.filter(published=True)


class MemorialView(DetailView):

    model = models.Memorial
    context_object_name = 'memorial'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        data = self.get_context_data(object=self.object)
        if request.META['HTTP_ACCEPT'] == 'application/json':
            return HttpResponseRedirect(reverse('memorial-json', kwargs={'slug': self.object.slug}))
        return self.render_to_response(data)

    def dispatch(self, *args, **kwargs):
        response = super(MemorialView, self).dispatch(*args, **kwargs)
        response['Link'] = '<' + self.object.get_absolute_url() + '>; rel="canonical", <' + self.object.get_json_url() + '>; rel="alternate"; type="application/json"'

        return response


class MemorialJsonView(DetailView):

    model = models.Memorial
    context_object_name = 'memorial'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        absolute_url = request.build_absolute_uri(self.object.get_absolute_url())

        data = {
            'id': self.object.slug,
            'url': absolute_url,
            'name': self.object.pretty_name,
            'created': self.object.created_at,
            'updated': self.object.updated_at,
            'names': []
        }

        for name in self.object.names.all():
            data['names'].append({
                'name': name.__str__(),
                'family_name': name.family_name,
                'given_names': name.given_names,
                'date_of_birth': name.date_of_birth,
                'date_of_death': name.date_of_death
            })

        response = JsonResponse(data)

        response['Link'] = '<' + self.object.get_absolute_url() + '>; rel="canonical", <' + self.object.get_absolute_url() + '>; rel="alternate"; type="text/html"'

        return response


class NameListView(ListView):

    model = models.Name
    paginate_by = 50
    context_object_name = 'names'


class NameView(DetailView):

    model = models.Name
    context_object_name = 'name'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        data = self.get_context_data(object=self.object)
        if request.META['HTTP_ACCEPT'] == 'application/json':
            return HttpResponseRedirect(reverse('name-json', kwargs={'slug': self.object.slug}))
        return self.render_to_response(data)

    def dispatch(self, *args, **kwargs):
        response = super(NameView, self).dispatch(*args, **kwargs)
        response['Link'] = '<' + self.object.get_absolute_url() + '>; rel="canonical", <' + self.object.get_json_url() + '>; rel="alternate"; type="application/json"'

        return response


class NameJsonView(DetailView):

    model = models.Name
    context_object_name = 'name'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        absolute_url = request.build_absolute_uri(self.object.get_absolute_url())

        data = {
            'id': self.object.slug,
            'url': absolute_url,
            'created': self.object.created_at,
            'updated': self.object.updated_at
        }

        response = JsonResponse(data)

        response['Link'] = '<' + self.object.get_absolute_url() + '>; rel="canonical", <' + self.object.get_absolute_url() + '>; rel="alternate"; type="text/html"'

        return response
