from django.contrib import admin

from gardens.models import Garden


# Register your models here.
class GardenAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name', 'description']
    readonly_fields = ["slug", "creation", "updated"]


admin.site.register(Garden, GardenAdmin)
