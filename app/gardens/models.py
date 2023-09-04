from django.db import models
from django.db.models.signals import pre_save, post_save

from gardens.utils import slugify_instance_name


# Create your models here.
class Garden(models.Model):
    name = models.CharField(max_length=128)
    slug = models.SlugField(unique=True, blank=True, null=True)
    description = models.TextField()
    creation = models.DateField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # if self.slug is None:
        #     self.slug = slugify(self.name)
        super().save(*args, **kwargs)


def garden_pre_save(sender, instance, *args, **kwargs):
    if instance.slug is None:
        slugify_instance_name(instance, save=False)


pre_save.connect(garden_pre_save, sender=Garden)


def garden_post_save(sender, instance, created, *args, **kwargs):
    if created:
        slugify_instance_name(instance, save=True)


post_save.connect(garden_post_save, sender=Garden)
