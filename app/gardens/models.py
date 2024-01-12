from datetime import datetime, timedelta, timezone

import pint
from django.conf import settings
from django.db import models
from django.db.models import Q
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.urls import reverse

from gardens import utils
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


class GardenQuerySet(models.QuerySet):
    def search(self, query):
        if query is None or query == '':
            return self.none()
        lookups = Q(name__icontains=query) | Q(description__icontains=query)
        return self.filter(lookups)


class GardenManager(models.Manager):
    def get_queryset(self):
        return GardenQuerySet(self.model, using=self._db)

    def search(self, query):
        return self.get_queryset().search(query=query)


class Garden(models.Model):
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, related_name='gardens')
    name = models.CharField(max_length=128)
    slug = models.SlugField(unique=True, blank=True, null=True)
    description = models.TextField()
    creation = models.DateField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = GardenManager()

    def get_absolute_url(self):
        return reverse('gardens:detail', kwargs={'slug': self.slug})

    def get_edit_url(self):
        return reverse('gardens:edit', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('gardens:delete', kwargs={'slug': self.slug})

    def get_amendment_children(self, order='desc'):
        qs = self.fertilizationinline_set.all()
        return qs.order_by('-due_date') if order == 'desc' else qs.order_by('due_date')


@receiver(pre_save, sender=Garden)
def pre_save_receiver(sender, instance, *args, **kwargs):
    if instance.slug is None:
        utils.slugify_instance_name(instance, save=False)


@receiver(post_save, sender=Garden)
def post_save_receiver(sender, instance, created: bool, *args, **kwargs):
    if created:
        utils.slugify_instance_name(instance, save=True)


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
            return f"Il y a {time_difference.total_seconds() // 60}min"
        elif time_difference < timedelta(days=1):
            hours = int(time_difference.total_seconds() // 3600)
            return f"Il y a {hours}h"
        else:
            return f"Il y a {time_difference.days}j.\n({self.due_date.strftime('%d.%-m.%y')})"

    def convert_to_system(self, system="mks"):
        if self.quantity_as_float is None:
            return None
        ureg = pint.UnitRegistry(system=system)
        return self.quantity_as_float * ureg[self.unit.lower()]

    def as_mks(self):
        # meter, kilogram, second
        measurement = self.convert_to_system(system='mks')
        return "{:~}".format(measurement.to_base_units())

    def get_quantity(self, system="mks"):
        if system == "mks":
            return self.as_mks()
        elif system == "imperial":
            return self.as_imperial()

    def as_imperial(self):
        # miles, pounds, seconds
        measurement = self.convert_to_system(system='imperial')
        return measurement.to_base_units()

    def get_nitrogen_quantity(self):
        # TODO: required to add the product percentage
        pass

    def get_hx_edit_url(self):
        kwargs = {
            'parent_id': self.garden.id,
            'id': self.id
        }
        return reverse('gardens:hx-amendment-detail', kwargs=kwargs)
