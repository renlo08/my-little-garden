from datetime import datetime, timedelta, timezone

import pint
from django.conf import settings
from django.db import models
from django.urls import reverse

from gardens.validators import validate_unit_measurement

User = settings.AUTH_USER_MODEL


class FertilizerComponent(models.Model):
    name = models.CharField(max_length=4)
    percentage = models.IntegerField()
    details = models.TextField()


class Fertilizer(models.Model):
    name = models.CharField(max_length=90)
    producer = models.CharField(max_length=30)
    organic = models.BooleanField(default=False)
    components = models.ManyToManyField(FertilizerComponent)


class Garden(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=128)
    slug = models.SlugField(unique=True, blank=True, null=True)
    description = models.TextField()
    creation = models.DateField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse('gardens:detail', kwargs={'id': self.id})

    def get_edit_url(self):
        return reverse('gardens:update', kwargs={'id': self.id})

    def get_delete_url(self):
        return reverse('gardens:delete', kwargs={'id': self.id})

    def get_fertilizations_children(self, order='desc'):
        qs = self.fertilizationinline_set.all()
        if order == 'desc':
            return qs.order_by('-due_date')
        return qs.order_by('due_date')


class FertilizationInline(models.Model):
    garden = models.ForeignKey(Garden, on_delete=models.CASCADE)
    due_date = models.DateTimeField()
    quantity_as_float = models.FloatField(null=True, blank=True)
    unit = models.CharField(max_length=50, validators=[validate_unit_measurement], blank=True, null=True)
    # fertilizer = models.ForeignKey(Fertilizer, on_delete=models.SET_NULL, null=True)

    def since_creation_timestamp(self):
        current_time = datetime.now(tz=timezone.utc)  # This is timezone-aware
        time_difference = current_time - self.due_date

        if time_difference < timedelta(hours=1):
            return "Moins d´une heure"
        elif time_difference < timedelta(days=1):
            hours = int(time_difference.total_seconds() // 3600)
            return f"{hours}h"
        else:
            days = time_difference.days
            return f"{days} jours"

    def convert_to_system(self, system="mks"):
        if self.quantity_as_float is None:
            return None
        ureg = pint.UnitRegistry(system=system)
        measurement = self.quantity_as_float * ureg[self.unit.lower()]
        return measurement

    def as_mks(self):
        # meter, kilogram, second
        measurement = self.convert_to_system(system='mks')
        return measurement.to_base_units()

    def as_imperial(self):
        # miles, pounds, seconds
        measurement = self.convert_to_system(system='imperial')
        return measurement.to_base_units()

    def get_nitrogen_quantity(self):
        # TODO: required to add the product percentage
        pass