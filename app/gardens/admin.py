from django.contrib import admin

from gardens.models import Garden, Address


class GardenAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name', 'description']
    readonly_fields = ["slug", "creation", "updated"]


# Register the model and admin class
admin.site.register(Garden, GardenAdmin)


class AddressAdmin(admin.ModelAdmin):
    list_display = ['name', 'city', 'street', 'postal_code', 'country']
    readonly_fields = ["latitude", "longitude"]


# Register the model and admin class
admin.site.register(Address, AddressAdmin)
