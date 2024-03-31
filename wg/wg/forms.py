from django import forms
from django.forms import widgets
from django.utils.safestring import mark_safe
from django.template import loader
from app.models import *

class DishForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Gerichtname',
                                                         'class': 'form-headline'}), required=True, label='')
    dishType = forms.ModelChoiceField(queryset=DishType.objects.all(), required=True, label='', widget=forms.Select(attrs={'class': 'form-choicefield'}))
    chef = forms.ModelChoiceField(queryset=User.objects.all(), required=False, label='', widget=forms.Select(attrs={'class': 'form-choicefield'}))
    proximityDuration = forms.IntegerField(widget=forms.NumberInput(attrs={'placeholder': 'min.', 'class': 'form-number'}), label='', max_value=999, required=True, label_suffix='Minuten')
    description = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Zubereitungsbeschreibung', 'class': 'form-textfield'},), label='', required=False)

    class Meta:
        model = Dish
        fields = ('name', 'proximityDuration', 'dishType', 'description', 'chef')


class DishplanSettingsForm(forms.ModelForm):
    dishType = forms.ModelChoiceField(queryset=DishType.objects.all(), required=True, label='', widget=forms.Select(attrs={'class': 'form-choicefield'}))

    class Meta:
        model = DishplanSettings
        fields = ('dishType', )
    
    def save(self):
        print(self)
        item = super(DishplanSettingsForm, self).save(commit=False)
        item.dishType = self.cleaned_data['dishType']
        item.save()

class CustomCheckboxInput(forms.CheckboxInput):
    template_name = "checkbox.html"

FREQUENCY_CHOICES = [(0, "Einmalig"), (7, "Wöchentlich"), (14, "Alle zwei Wochen"), (30, "Monatlich")]
WEEKDAY_CHOICES = [(0, "Montag"), (1, "Dienstag"), (2, "Mittwoch"), (3, "Donnerstag"), (4, "Freitag"), (5, "Samstag"), (6, "Sonntag")]

class TaskForm(forms.ModelForm):
    title = forms.CharField(required=True, label='', widget=forms.TextInput(attrs={'placeholder': 'Aufgabe', 'class': 'form-headline'}))
    responsibility = forms.ModelChoiceField(queryset=User.objects.all(), required=True, label='', widget=forms.Select(attrs={'class': 'form-choicefield'}))
    points = forms.IntegerField(required=True, label='', widget=forms.NumberInput(attrs={'placeholder': 'Punkte', 'class': 'form-number'}))
    isDone = forms.BooleanField(required=False, label='', widget=CustomCheckboxInput())
    frequency = forms.ChoiceField(choices=FREQUENCY_CHOICES, label='', widget=forms.Select(attrs={'class': 'form-choicefield'}))
    weekday = forms.ChoiceField(choices=WEEKDAY_CHOICES, label='', widget=forms.Select(attrs={'class': 'form-choicefield'}))
    
    class Meta:
        model = Task
        fields = ('isDone', 'title', 'points', 'responsibility', 'frequency', 'weekday')


class TaskCheckboxForm(forms.ModelForm):
    isDone = forms.BooleanField(required=False, label='', widget=CustomCheckboxInput(attrs={'onclick': 'this.form.submit();'}))

    class Meta:
        model = Task
        fields = ('isDone',)
    