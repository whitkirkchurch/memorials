"""memorials URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from core.admin import memorialsadmin
from django.urls import include, path

from django.contrib.sitemaps.views import sitemap

from core.models import Memorial, Tag, Location, Name

from django.contrib.sitemaps import Sitemap


class MemorialsSitemap(Sitemap):
    changefreq = "yearly"
    protocol = "https"

    def items(self):
        return Memorial.objects.filter(published=True)

    @classmethod
    def lastmod(cls, obj):
        return obj.updated_at


class NamesSitemap(Sitemap):
    changefreq = "yearly"
    protocol = "https"

    def items(self):
        return Name.objects.all()

    @classmethod
    def lastmod(cls, obj):
        return obj.updated_at


class TagsSitemap(Sitemap):
    changefreq = "yearly"
    protocol = "https"

    def items(self):
        return Tag.objects.all()


class LocationsSitemap(Sitemap):
    changefreq = "yearly"
    protocol = "https"

    def items(self):
        return Location.objects.all()


sitemaps = {
    "memorials": MemorialsSitemap,
    "names": NamesSitemap,
    "tags": TagsSitemap,
    "locations": LocationsSitemap,
}

urlpatterns = [
    path("", include("core.urls")),
    path("markdownx/", include("markdownx.urls")),
    path("admin/", memorialsadmin.urls),
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.sitemap",
    ),
]
