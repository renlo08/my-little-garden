from django.db import models

# Create your models here.
class Garden(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField()