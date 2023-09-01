from django.db import models
from django.db.models.signals import pre_save, post_save
from django.urls import reverse
from django.utils.text import slugify


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
        instance.slug = slugify(instance.name)
    print('pre_save')
    print(args, kwargs)

pre_save.connect(garden_pre_save, sender=Garden)

def garden_post_save(sender, instance, created, *args, **kwargs):
    if created:
        instance.slug = slugify(instance.name)
        instance.save()

post_save.connect(garden_post_save, sender=Garden)