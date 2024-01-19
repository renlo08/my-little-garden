from django.contrib import admin

from activities.models import Fertilization, Activity


# Register your models here.

class FertilizationAdmin(admin.ModelAdmin):
    list_display = ('quantity_as_float',)
    search_fields = ('quantity_as_float',)


# Register the model and admin class
admin.site.register(Fertilization, FertilizationAdmin)


class ActivityAdmin(admin.ModelAdmin):
    list_display = ('creation', 'activity', 'garden', 'fertilization')
    search_fields = ('activity',)
    readonly_fields = ('updated',)


# Register the model and admin class
admin.site.register(Activity, ActivityAdmin)
