from django import forms
from gardens.models import Garden


class GardenForm(forms.ModelForm):
    class Meta:
        model = Garden
        fields = ['name', 'description']

    def clean(self):
        data = self.cleaned_data
        garden_name = data.get('name')
        qs = Garden.objects.filter(name__icontains=garden_name)
        if qs.exists():
            self.add_error("name", f"'{garden_name}' is already in use. Please pick another garden name.")
        return data
