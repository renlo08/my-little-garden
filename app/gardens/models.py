from datetime import datetime, timedelta, timezone

import pint
from django.conf import settings
from django.db import models
from django.db.models import Q
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.urls import reverse
from enumfields import EnumField
from geopy import Nominatim

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


class Address(models.Model):
    name = models.CharField(max_length=60)
    street = models.CharField(max_length=60, blank=True, null=True)
    house_number = models.CharField(max_length=10, blank=True, null=True)
    city = models.CharField(max_length=60, blank=True, null=True)
    state = models.CharField(max_length=60, blank=True, null=True)
    postal_code = models.CharField(max_length=10, blank=True, null=True)
    country = models.CharField(max_length=30, blank=True, null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.latitude or not self.longitude:
            self.get_lat_lon()
        super().save(*args, **kwargs)

    def get_lat_lon(self):
        address_string = f"{self.street} {self.house_number}, {self.city}, {self.postal_code}"
        geolocator = Nominatim(user_agent="myLittleGardenApp")
        location = geolocator.geocode(address_string)

        if location:
            self.latitude = location.latitude
            self.longitude = location.longitude


class GardenOwner(models.Model):
    gender = EnumField(utils.Gender, max_length=1)
    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)


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
    address = models.ForeignKey(Address, on_delete=models.CASCADE, related_name='gardens', null=True, blank=True)

    objects = GardenManager()

    def has_garden(self):
        return self.address is not None

    def get_last_update(self):
        return compute_time_difference(self.updated)

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
        return compute_time_difference(self.due_date)

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


def compute_time_difference(date: datetime):
    current_time = datetime.now(tz=timezone.utc)  # This is timezone-aware
    time_difference = current_time - date

    if time_difference < timedelta(hours=1):
        minutes = int(time_difference.total_seconds() / 60)
        return f"Il y a {minutes}min"
    elif time_difference < timedelta(days=1):
        hours = int(time_difference.total_seconds() // 3600)
        return f"Il y a {hours}h"
    else:
        return f"Il y a {time_difference.days}j.\n({date.strftime('%d.%-m.%y')})"
