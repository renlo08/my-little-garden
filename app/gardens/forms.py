from django import forms

from gardens.models import Garden, Fertilizer, FertilizationInline


class FertilizerForm(forms.ModelForm):
    class Meta:
        model = Fertilizer
        fields = ['name', 'producer', 'organic']

    def clean(self):
        data = self.cleaned_data
        fertilizer_name = data.get('name')
        qs = Fertilizer.objects.filter(name__exact=fertilizer_name)
        if qs.exists():
            raise forms.ValidationError('This fertilizer already exists')
        return data


class FertilizationForm(forms.ModelForm):
    class Meta:
        model = FertilizationInline
        fields = ['due_date', 'quantity_as_float', 'unit']


class GardenForm(forms.ModelForm):
    class Meta:
        model = Garden
        fields = ['name', 'description']

    def clean(self):
        data = self.cleaned_data
        garden_name = data.get('name')
        qs = Garden.objects.filter(name__icontains=garden_name)
        if qs.exists():
            self.add_error("name", f"'{garden_name}' est déjà utilisé. Veuillez choisir un autre nom de jardin.")
        return data
