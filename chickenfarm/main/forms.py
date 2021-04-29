from django import forms
from django.forms.models import modelformset_factory
from . import models

class MedicineForm(forms.ModelForm):
    class Meta:
        model = models.Medicine
        exclude = ['farm', 'timestamp']
        
class FoodForm(forms.ModelForm):
    class Meta:
        model = models.Food
        exclude = ['farm', 'timestamp']

class SwitchForm(forms.ModelForm):
    value= forms.BooleanField(required=True)
    class Meta:
        model = models.Switch
        exclude = ['device','comment']
        widgets = {
            'name': forms.TextInput(attrs={'cols': 80, 'rows': 20, 'readonly': True}),
        }


class ReadingForm(forms.ModelForm):
    class Meta:
        model = models.Reading
        exclude = ['device','comment']
        widgets = {
            'name': forms.TextInput(attrs={'cols': 80, 'rows': 20, 'readonly': True}),
        }

# SwitchFormSet = modelformset_factory(
#     models.Switch,
#     exclude = ['device','comment'],
#     extra=1,
#     widgets={
#         'name': forms.TextInput(attrs={'readonly': True}),
#     }
# )