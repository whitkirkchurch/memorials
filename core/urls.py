from django.urls import path

from . import views

urlpatterns = [
    path('', views.index.as_view(), name='index'),

    path('locations', views.LocationListView.as_view(), name='locations'),
    path('locations/<pk>', views.LocationView.as_view(), name='location'),

    path('memorials', views.MemorialListView.as_view(), name='memorials'),
    path('memorials/<slug:slug>', views.MemorialView.as_view(), name='memorial'),

    path('names', views.NameListView.as_view(), name='names')
]
