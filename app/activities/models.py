# Create your models here.
from django.db import models

from gardens.models import Garden


class ActivityChoices(models.TextChoices):
    FERTILIZE = "F", "Fertilisation"
    PLANT = "P", "Plantation"
    CUT = "C", "Taille"


class Activity(models.Model):
    activity = models.CharField(max_length=1, choices=ActivityChoices.choices)
    comment = models.TextField()
    garden = models.ForeignKey(Garden, on_delete=models.CASCADE, related_name='activities', null=True, blank=True)

    def __str__(self):
        return self.activity
