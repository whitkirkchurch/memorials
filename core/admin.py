from django.contrib import admin

from core import models


class LocationAdmin(admin.ModelAdmin):
    list_display = ('name',)

admin.site.register(models.Location, LocationAdmin)


class NameInline(admin.TabularInline):
    model = models.Name


class MemorialAdmin(admin.ModelAdmin):

    list_display = ('pretty_name', 'names_on_memorial', 'location')

    inlines = [
        NameInline,
    ]

admin.site.register(models.Memorial, MemorialAdmin)


class NameAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'date_of_birth', 'date_of_death', 'memorial_name', 'memorial_location')

    def memorial_name(self, obj):
        return obj.memorial.pretty_name()
    memorial_name.admin_order_field = 'memorial__name'

    def memorial_location(self, obj):
        return obj.memorial.location.name
    memorial_location.admin_order_field = 'memorial__location__name'

admin.site.register(models.Name, NameAdmin)
