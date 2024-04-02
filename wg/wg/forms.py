from django import forms
from django.forms import widgets
from django.utils.safestring import mark_safe
from django.template import loader
from app.models import *
import datetime

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
        item = super(DishplanSettingsForm, self).save(commit=False)
        item.dishType = self.cleaned_data['dishType']
        item.save()

class CustomCheckboxInput(forms.CheckboxInput):
    template_name = "checkbox.html"

FREQUENCY_CHOICES = [(0, "Einmalig"), (7, "Wöchentlich"), (14, "Alle zwei Wochen"), (30, "Monatlich")]

class TaskForm(forms.ModelForm):
    title = forms.CharField(required=True, label='', widget=forms.TextInput(attrs={'id': 'title', 'placeholder': 'Aufgabe', 'class': 'form-headline'}))
    responsibility = forms.ModelChoiceField(queryset=User.objects.all(), required=True, label='Nächste Zuständigkeitsperson', widget=forms.Select(attrs={'id': 'responsibility','class': 'form-choicefield'}))
    points = forms.IntegerField(required=True, label='Punkte', widget=forms.NumberInput(attrs={'id': 'points', 'placeholder': 'Punkte', 'class': 'form-number'}))
    frequency = forms.ChoiceField(choices=FREQUENCY_CHOICES, label='Wiederholen', widget=forms.Select(attrs={'id': 'frequency', 'class': 'form-choicefield'}))
    deadlineDate = forms.DateField(label='Startdatum', widget=forms.DateInput(format=('%Y-%m-%d'), attrs={'id': 'startDate','type': 'date', 'value': datetime.date.today}))
    
    class Meta:
        model = Task
        fields = ('title', 'points', 'responsibility', 'deadlineDate', 'frequency')

    def save(self, commit=True):
        task = super(TaskForm, self).save(commit=False)
        task.title = self.cleaned_data['title']
        task.responsibility = self.cleaned_data['responsibility']
        task.points = self.cleaned_data['points']
        task.frequency = self.cleaned_data['frequency']
        task.deadlineDate = self.cleaned_data['deadlineDate']
        task.lastChangeDate = datetime.datetime.now().strftime('%Y-%m-%d')
        task.save()


class TaskCheckboxForm(forms.ModelForm):
    isDone = forms.BooleanField(required=False, label='', widget=CustomCheckboxInput(attrs={'onclick': 'this.form.submit();'}))

    class Meta:
        model = Task
        fields = ('isDone',)

    def save(self, commit=True):
        task = super(TaskCheckboxForm, self).save(commit=False)
        task_obj = Task.objects.get(pk=self.instance.id_task)
        task.isDone = self.cleaned_data['isDone']
        if task_obj.isDone != 1:
            task.save()
        if task.isDone == True:
            new_task = Task.objects.get(pk=self.instance.id_task)
            today = datetime.datetime.strptime(datetime.datetime.now().strftime('%Y-%m-%d'), '%Y-%m-%d')
            old_deadline = datetime.datetime.strptime(new_task.deadlineDate.strftime('%Y-%m-%d'), '%Y-%m-%d')

            if new_task.frequency == 0: #EINMALIG
                deadlineDate = None
            elif new_task.frequency == 30: #MONATLICH
                day = old_deadline.day
                if old_deadline < today: #Wenn Deadline in der Vergangenheit
                    if today.month == 12:
                        month = 1
                        year = today.year + 1
                    else:
                        month = today.month + 1
                        year = today.year
                    new_date = datetime.datetime(year=year, month=month, day=day)
                else: #Wenn Deadline in der Zukunft
                    if old_deadline.month == 12: 
                        month = 1
                        year = old_deadline.year + 1
                    else:
                        month = old_deadline.month + 1
                        year = old_deadline.year
                    new_date = datetime.datetime(year=year, month=month, day=day)
            else: #WÖCHENTLICH BZW. ZWEIWÖCHENTLICH
                freq = new_task.frequency
                new_date = old_deadline + datetime.timedelta(days=freq)
                if new_date < today:
                    weekday_delta = old_deadline.weekday() - today.weekday()
                    if weekday_delta < 0:
                        weekday_delta += 7        
                    new_date = today + datetime.timedelta(days=weekday_delta)
                    
            Task.objects.create(title=new_task.title, 
                                frequency=new_task.frequency,
                                responsibility = new_task.responsibility,
                                deadlineDate = new_date,
                                points = new_task.points)