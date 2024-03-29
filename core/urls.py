from django.urls import path

from . import views

urlpatterns = [
    path("", views.index.as_view(), name="home"),
    path("about", views.about.as_view(), name="about"),
    path("disclaimer", views.Disclaimer.as_view(), name="disclaimer"),
    path("locations", views.LocationListView.as_view(), name="locations"),
    path("locations/<slug>", views.LocationView.as_view(), name="location"),
    path("collections", views.TagListView.as_view(), name="tags"),
    path("collections/<slug>", views.TagView.as_view(), name="tag"),
    path("memorials", views.MemorialListView.as_view(), name="memorials"),
    path(
        "memorials/<slug>.json", views.MemorialJsonView.as_view(), name="memorial-json"
    ),
    path("memorials/<slug>", views.MemorialView.as_view(), name="memorial"),
    path("names", views.NameListView.as_view(), name="names"),
    path("names/<slug>.json", views.NameJsonView.as_view(), name="name-json"),
    path("names/<slug>", views.NameView.as_view(), name="name"),
]
