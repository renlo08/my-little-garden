from django import forms

from activities.models import Fertilization


class FertilizationForm(forms.ModelForm):
    class Meta:
        model = Fertilization
        fields = ['due_date', 'quantity_as_float', 'unit']