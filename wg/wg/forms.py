from django import forms
from app.models import *


class DishForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput, required=True)
    proximityDuration = forms.IntegerField(widget=forms.NumberInput)
    description = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Dish
        fields = ('name', 'proximityDuration', 'description')
