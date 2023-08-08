from django.db import models

# Create your models here.


class Garden(models.Model):
    """
    Store the items related to the garden
    """
    name = models.CharField(max_length=60)
    slug = models.SlugField()


class Task(models.Model):
    """
    Store the items related to a specific garden
    """
    description = models.CharField(max_length=300)
    garden = models.ForeignKey(Garden, on_delete=models.CASCADE)
