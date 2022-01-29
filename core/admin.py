from django.contrib import admin

from django.contrib.admin import AdminSite

from markdownx.admin import MarkdownxModelAdmin

from . import models


class MemorialsAdminSite(AdminSite):
    site_header = "Memorials administration"
    site_title = "Memorials administration"


memorialsadmin = MemorialsAdminSite(name="memorialsadmin")


class LocationAdmin(MarkdownxModelAdmin):
    list_display = ("name",)


memorialsadmin.register(models.Location, LocationAdmin)


class TagAdmin(MarkdownxModelAdmin):
    list_display = ("name", "slug")


memorialsadmin.register(models.Tag, TagAdmin)


class NameMemorialInline(admin.TabularInline):
    model = models.Memorial.names.through


class MemorialImageInline(admin.StackedInline):
    model = models.MemorialImage


def mark_published(modeladmin, request, queryset):
    queryset.update(published=True)


mark_published.short_description = "Mark selected memorials as published"


def mark_unpublished(modeladmin, request, queryset):
    queryset.update(published=False)


mark_unpublished.short_description = "Mark selected memorials as unpublished"


class MemorialAdmin(MarkdownxModelAdmin):

    list_display = (
        "slug",
        "pretty_name",
        "names_on_memorial",
        "location",
        "complete",
        "published",
    )

    readonly_fields = ("slug",)

    list_filter = ("location", "complete", "published", "tags")

    search_fields = ("slug", "pretty_name")

    exclude = ("names",)

    inlines = [NameMemorialInline, MemorialImageInline]

    actions = [mark_published, mark_unpublished]


memorialsadmin.register(models.Memorial, MemorialAdmin)


class NameAdmin(admin.ModelAdmin):
    list_display = ("__str__", "slug", "date_of_birth", "date_of_death")

    search_fields = ("given_names", "family_name", "slug")

    readonly_fields = ("slug",)


memorialsadmin.register(models.Name, NameAdmin)


memorialsadmin.register(models.MemorialImage)
