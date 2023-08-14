from django.contrib import admin

from gardens.models import Garden

# Register your models here.
class GardenAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']

admin.site.register(Garden, GardenAdmin)