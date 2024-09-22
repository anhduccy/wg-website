from django import forms
from django.forms import widgets
from django.utils.safestring import mark_safe
from django.template import loader
from app.models import *
from app.functions import *
from app.task_log_event import *

import datetime, operator


class DishForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'id': 'name', 'placeholder': 'Gerichtname',
                                                         'class': 'form-headline'}), required=True, label='')
    dishType = forms.ModelChoiceField(queryset=DishType.objects.all(), required=True, label='Gerichtsart', widget=forms.Select(attrs={'id': 'dishType', 'class': 'form-choicefield'}), empty_label=None)
    chef = forms.ModelChoiceField(queryset=User.objects.all(), required=False, label='Chefkoch', widget=forms.Select(attrs={'id': 'chef', 'class': 'form-choicefield'}), empty_label=None)
    proximityDuration = forms.IntegerField(widget=forms.NumberInput(attrs={'id': 'proximityDuration', 'placeholder': 'Dauer', 'class': 'form-number'}), label='', max_value=999, required=True, label_suffix='Minuten')
    description = forms.CharField(widget=forms.Textarea(attrs={'id': 'description', 'placeholder': 'Zubereitungsbeschreibung', 'class': 'form-textfield'},), label='', required=False)

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


FREQUENCY_CHOICES = [(0, "Einmalig"), (7, "Wöchentlich"), (14, "Alle zwei Wochen"), (30, "Monatlich"), (-1, "Bei Bedarf")]
class TaskAddForm(forms.ModelForm):
    title = forms.CharField(required=True, label='', widget=forms.TextInput(attrs={'id': 'title', 'placeholder': 'Aufgabe', 'class': 'form-headline'}))
    responsibility = forms.ModelChoiceField(queryset=User.objects.all(), required=True, label='Nächste Zuständigkeitsperson', widget=forms.Select(attrs={'id': 'responsibility','class': 'form-choicefield'}), empty_label=None)
    points = forms.IntegerField(required=True, label='Punkte', widget=forms.NumberInput(attrs={'id': 'points', 'placeholder': 'Punkte', 'class': 'form-number'}))
    frequency = forms.ChoiceField(choices=FREQUENCY_CHOICES, label='Wiederholen', widget=forms.Select(attrs={'id': 'frequency', 'class': 'form-choicefield'}))
    deadlineDate = forms.DateField(label='', widget=forms.DateInput(format=('%Y-%m-%d'), attrs={'id': 'deadlineDate','type': 'date', 'value': datetime.date.today}))
    
    class Meta:
        model = Task
        fields = ('title', 'points', 'responsibility', 'frequency', 'deadlineDate')
    
    def save(self, request, commit=True):
        task = super(TaskAddForm, self).save(commit=False)
        task.title = self.cleaned_data['title']
        task.points = self.cleaned_data['points']
        task.responsibility = self.cleaned_data['responsibility']
        task.deadlineDate = self.cleaned_data['deadlineDate']
        task.frequency = self.cleaned_data['frequency']
        task.creationDate = datetime.datetime.now()
        task.lastChangeDate = datetime.datetime.now()
        task.save()
        TaskLogEvent.objects.create(event=TaskLogEventDescription.added.value, task=task, ipAddress=getIP(request))


class TaskEditForm(TaskAddForm):
    def save(self, request, commit=True):
        task = super(TaskAddForm, self).save(commit=False)
        try: 
            taskObj = Task.objects.get(pk=self.instance.id_task)
            task.title = self.cleaned_data['title']
            task.points = self.cleaned_data['points']
            task.responsibility = self.cleaned_data['responsibility']
            task.deadlineDate = self.cleaned_data['deadlineDate']
            task.frequency = self.cleaned_data['frequency']
            task.lastChangeDate = datetime.datetime.now()
            task.save()
            ip = getIP(request)

            if str(taskObj.title) != str(task.title):
                event = "Titel geändert: " + taskObj.title +" -> " + task.title
                TaskLogEvent.objects.create(event=event, task=task, ipAddress=ip)

            if str(taskObj.points) != str(task.points):
                event = "Punkte geändert: " + str(taskObj.points) + " -> " + str(task.points)
                TaskLogEvent.objects.create(event=event, task=task, ipAddress=ip)

            if str(taskObj.responsibility) != str(task.responsibility):
                event = "Zuständigkeitsperson geändert: " + str(taskObj.responsibility) + " -> " + str(task.responsibility)
                TaskLogEvent.objects.create(event=event, task=task, ipAddress=ip)

            if taskObj.deadlineDate.strftime("%Y-%m-%d") != task.deadlineDate.strftime("%Y-%m-%d"):
                event = "Fälligkeitsdatum geändert: " + taskObj.deadlineDate.strftime("%d.%m.%Y") + " -> " + task.deadlineDate.strftime("%d.%m.%Y")
                TaskLogEvent.objects.create(event=event, task=task, ipAddress=ip)

            if str(taskObj.frequency) != str(task.frequency):
                d = dict(FREQUENCY_CHOICES)
                freqObj = d.get(taskObj.frequency)
                freq = d.get(int(task.frequency))
                event = "Wiederholungsfrequenz geändert: " + freqObj + " -> " + freq
                TaskLogEvent.objects.create(event=event, task=task, ipAddress=ip)
        except:
            return


class TaskCheckboxForm(forms.ModelForm):
    isDone = forms.BooleanField(required=False, label='', widget=CustomCheckboxInput(attrs={'onclick': 'this.form.submit();'}))

    class Meta:
        model = Task
        fields = ('isDone',)
    
    def monthly(today):
        if today.month == 12:
            month = 1
            year = today.year + 1
        else:
            month = today.month + 1
            year = today.year
        new_date = datetime.datetime(year=year, month=month, day=today.day)
        return new_date
    
    def weekly(new_task, today):
        freq = new_task.frequency
        new_date = today + datetime.timedelta(days=freq)
        return new_date
    
    def getNextResponsibility():
        leaderboard = []
        for user in User.objects.all():
            mock_user = [user, user.points]
            try:
                tasks = Task.objects.filter(isDone=0, responsibility=mock_user[0])
            except:
                print("ERROR forms.py: Die Person mit der ID: ", mock_user[0], "hat keine Aufgaben zugewiesen bekommen")
            for upcoming_task in tasks:
                mock_user[1] += 1
            leaderboard.append(mock_user)
        leaderboard_sorted = sorted(leaderboard, key=operator.itemgetter(1))
        return leaderboard_sorted[0][0]

    def save(self, request, commit=True):
        task = super(TaskCheckboxForm, self).save(commit=False)
        task_obj = Task.objects.get(pk=self.instance.id_task)
        task.isDone = self.cleaned_data['isDone']

        if task_obj.isDone != 1 and task.isDone == True:
            task.lastChangeDate = datetime.datetime.now() #DATE AND TIMESTAMP
            task.save()
            TaskLogEvent.objects.create(event=TaskLogEventDescription.isDone_changed.value, task=task, ipAddress=getIP(request))

            #POINTS AWARD
            resp = User.objects.get(pk=task.responsibility.id_user)
            resp.points += task.points
            resp.save()

            new_task = Task.objects.get(pk=self.instance.id_task)
            today = datetime.datetime.strptime(datetime.datetime.now().strftime('%Y-%m-%d'), '%Y-%m-%d')
            
            if new_task.frequency == 0: #EINMALIG
                return
            elif new_task.frequency == -1: #BEI BEDARF
                new_date = datetime.date.today()
            elif new_task.frequency == 30: #MONATLICH
                new_date = TaskCheckboxForm.monthly(today)
            else: #WÖCHENTLICH BZW. ZWEIWÖCHENTLICH
                new_date = TaskCheckboxForm.weekly(new_task, today)
            
            new_task.responsibility = TaskCheckboxForm.getNextResponsibility()
                    
            Task.objects.create(title=new_task.title, 
                                frequency=new_task.frequency,
                                responsibility = new_task.responsibility,
                                deadlineDate = new_date,
                                points = new_task.points)
            
class TaskSearchForm(forms.Form):
     query = forms.CharField(label='', max_length=100, required=False, widget=forms.TextInput(attrs={'id': 'search', 'placeholder': 'Tippe ein und drücke Enter, um zu suchen', 'class': 'searchbar', 'size': '50'}))

class CurrencyInput(forms.NumberInput):
    template_name = "currency.html"

class TransactionForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'cell'}))
    sum = forms.DecimalField(widget=CurrencyInput(attrs={'class': 'cell'}))

    class Meta:
        model = Transaction
        fields = ('title', 'sum')

    def save(self, commit=True):
        transaction = super(TransactionForm, self).save(commit=False)
        try: 
            transactionObj = Transaction.objects.get(pk=transaction.id_transaction)
            if transactionObj.title == transaction.title and float(transactionObj.sum) == float(transaction.sum):
                pass
            else:
                transactionObj.isActive = 0
                transactionObj.save()
                Transaction.objects.create(title=transaction.title, sum=transaction.sum)
        except:
            transaction.title = self.cleaned_data["title"]
            transaction.sum = self.cleaned_data["sum"]
            transaction.save()


    def delete(self, request):
        try: obj = Transaction.objects.get(pk=request.get('delete'))
        except: print("TransactionFormError: Couldn't delete the transactions.")
        obj.isActive = 0
        obj.save()

