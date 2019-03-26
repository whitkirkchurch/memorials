from django.contrib import admin
from markdownx.admin import MarkdownxModelAdmin

from . import models


class LocationAdmin(MarkdownxModelAdmin):
    list_display = ('name',)


admin.site.register(models.Location, LocationAdmin)


class TagAdmin(MarkdownxModelAdmin):
    list_display = ('name', 'slug')


admin.site.register(models.Tag, TagAdmin)


class NameInline(admin.TabularInline):
    model = models.Name


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

    search_fields = ('slug', 'names_on_memorial', 'name')

    inlines = [
        NameInline, MemorialImageInline
    ]

    actions = [mark_published, mark_unpublished]


admin.site.register(models.Memorial, MemorialAdmin)


class NameAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'date_of_birth', 'date_of_death', 'memorial_name', 'memorial_location')

    search_fields = ('given_names', 'family_name')

    def memorial_name(self, obj):
        return obj.memorial.pretty_name
    memorial_name.admin_order_field = 'memorial__name'

    def memorial_location(self, obj):
        return obj.memorial.location.name
    memorial_location.admin_order_field = 'memorial__location__name'


admin.site.register(models.Name, NameAdmin)


admin.site.register(models.MemorialImage)
