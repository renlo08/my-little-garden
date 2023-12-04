from django.conf import settings
from django.db import models
from django.urls import reverse

User = settings.AUTH_USER_MODEL


class FertilizerComponent(models.Model):
    name = models.CharField(max_length=4)
    percentage = models.IntegerField()
    details = models.TextField()


class Fertilizer(models.Model):
    name = models.CharField(max_length=90)
    producer = models.CharField(max_length=30)
    is_ecologic = models.BooleanField(default=False)
    components = models.ManyToManyField(FertilizerComponent)


class GardenFertilization(models.Model):
    date = models.DateField()
    quantity = models.IntegerField()
    fertilizer = models.ForeignKey(Fertilizer, on_delete=models.SET_NULL, null=True)


class Garden(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=128)
    slug = models.SlugField(unique=True, blank=True, null=True)
    description = models.TextField()
    creation = models.DateField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    fertilisation = models.ForeignKey(GardenFertilization,
                                      on_delete=models.CASCADE,
                                      null=True)

    def get_absolute_url(self):
        return reverse('gardens:detail', kwargs={'id': self.id})

    def get_edit_url(self):
        return reverse('gardens:update', kwargs={'id': self.id})

    def get_delete_url(self):
        return reverse('gardens:delete', kwargs={'id': self.id})