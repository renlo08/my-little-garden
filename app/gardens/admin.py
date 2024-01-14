from django.contrib import admin

from gardens.models import Garden, FertilizationInline, Address


class FertilizationInlineAdmin(admin.ModelAdmin):
    list_display = ('garden', 'due_date', 'quantity_as_float')
    search_fields = ('garden', 'due_date')


# Register the model and admin class
admin.site.register(FertilizationInline, FertilizationInlineAdmin)


class GardenAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name', 'description']
    readonly_fields = ["slug", "creation", "updated"]

# Register the model and admin class
admin.site.register(Garden, GardenAdmin)


class AddressAdmin(admin.ModelAdmin):
    list_display = ['name', 'city', 'street', 'house_number', 'postal_code', 'country']
    readonly_fields = ["latitude", "longitude"]


# Register the model and admin class
admin.site.register(Address, AddressAdmin)