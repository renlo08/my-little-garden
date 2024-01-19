# Create your models here.
import pint
from django.db import models

from activities.validators import validate_unit_measurement
from app.utils import compute_time_difference
from gardens.models import Garden


class Fertilization(models.Model):
    quantity_as_float = models.FloatField(null=True, blank=True)
    unit = models.CharField(max_length=50, validators=[validate_unit_measurement], blank=True, null=True)

    def __str__(self):
        return f"{self.quantity_as_float}{self.unit}"

    def convert_to_system(self, system="mks"):
        if self.quantity_as_float is None:
            return None
        ureg = pint.UnitRegistry(system=system)
        return self.quantity_as_float * ureg[self.unit.lower()]

    def as_mks(self):
        # meter, kilogram, second
        measurement = self.convert_to_system(system='mks').to_base_units()
        number = measurement.magnitude
        unit = measurement.units
        formatted_number = "{:,.2f}".format(number).rstrip('0').rstrip('.').replace(",", ".")
        return "{} {:~}".format(formatted_number, unit)

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


class ActivityChoices(models.TextChoices):
    FERTILIZE = "F", "Fertilisation"
    PLANT = "P", "Plantation"
    CUT = "C", "Taille"


class Activity(models.Model):
    creation = models.DateTimeField()
    updated = models.DateTimeField(auto_now=True)
    activity = models.CharField(max_length=1, choices=ActivityChoices.choices)
    comment = models.TextField()
    garden = models.ForeignKey(Garden, on_delete=models.CASCADE, related_name='activities', null=True, blank=True)
    fertilization = models.OneToOneField(Fertilization, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.activity

    def get_creation_date(self):
        return self.creation.strftime('%d.%m.%y')

    def get_updated_date(self):
        return self.updated.strftime('%d.%m.%y')

    def since_update(self):
        return compute_time_difference(self.updated)

    def get_children_activity(self):
        if self.fertilization:
            return self.fertilization

    def get_quantity(self):
        if obj := self.get_children_activity():
            return obj.get_quantity()
        return '-'
