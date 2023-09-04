from django.contrib import admin

from gardens.models import Garden


# Register your models here.
class GardenAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'slug', 'creation', 'updated']
    search_fields = ['name', 'description']


admin.site.register(Garden, GardenAdmin)
