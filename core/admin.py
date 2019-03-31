from django.contrib import admin
from markdownx.admin import MarkdownxModelAdmin

from . import models


class LocationAdmin(MarkdownxModelAdmin):
    list_display = ('name',)


admin.site.register(models.Location, LocationAdmin)


class TagAdmin(MarkdownxModelAdmin):
    list_display = ('name', 'slug')


admin.site.register(models.Tag, TagAdmin)


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

    list_display = ('slug', 'pretty_name', 'names_on_memorial', 'location', 'complete', 'published')

    readonly_fields = ('slug',)

    list_filter = ('location', 'complete', 'published', 'tags')

    search_fields = ('slug', 'names_on_memorial', 'names')

    exclude = ('names',)

    inlines = [
        NameMemorialInline,
        MemorialImageInline
    ]

    actions = [mark_published, mark_unpublished]


admin.site.register(models.Memorial, MemorialAdmin)


class NameAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'date_of_birth', 'date_of_death')

    search_fields = ('given_names', 'family_name')


admin.site.register(models.Name, NameAdmin)


admin.site.register(models.MemorialImage)
