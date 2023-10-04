from django.conf import settings
from django.db import models
from django.db.models import Q
from django.db.models.signals import pre_save, post_save
from django.urls import reverse

from gardens.utils import slugify_instance_name

User = settings.AUTH_USER_MODEL


class GardenQuerySet(models.QuerySet):
    def search(self, query=None):
        if query is None or query=="":
            return self.none()
        lookups = Q(name__icontains=query) | Q(description__icontains=query)
        return self.filter(lookups)


class GardenManager(models.Manager):
    def get_queryset(self):
        return GardenQuerySet(self.model, using=self._db)

    def search(self, query=None):
        return self.get_queryset().search(query=query)


class Garden(models.Model):
    name = models.CharField(max_length=128)
    slug = models.SlugField(unique=True, blank=True, null=True)
    description = models.TextField()
    creation = models.DateField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = GardenManager()

    def get_absolute_url(self):
        return reverse('details-garden', kwargs={'slug':self.slug})

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


def garden_pre_save(sender, instance, *args, **kwargs):
    if instance.slug is None:
        slugify_instance_name(instance, save=False)


pre_save.connect(garden_pre_save, sender=Garden)


def garden_post_save(sender, instance, created, *args, **kwargs):
    if created:
        slugify_instance_name(instance, save=True)


post_save.connect(garden_post_save, sender=Garden)
