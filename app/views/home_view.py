from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader
from django.forms import modelformset_factory
from django.db.models import Q
from wg.forms import TaskCheckboxForm
from app.models import *
import datetime

def view(request):
    try:
        tasks = Task.objects.filter(~Q(frequency=-1) & Q(isDone=0) & Q(deadlineDate__lte=datetime.date.today())).order_by('deadlineDate')
        if tasks.count() == 0: 
            tasks = None
            formset = None
        else: 
            TaskFormSet = modelformset_factory(model=Task, form=TaskCheckboxForm, extra=0, fields = ('isDone',))
            formset = TaskFormSet(queryset=tasks)
            if request.method == "POST":
                formset = TaskFormSet(request.POST, queryset=tasks)
                if formset.is_valid():
                    for form in formset:
                        form.save()
                        return redirect('home')
            formset = TaskFormSet(queryset=tasks)
    except:
        formset = None

    try: 
        users = User.objects.all().order_by('-points')
        if users.count() == 0:
            usersTuple = None
        else:
            usersTuple = []
            index = 1
            for user in users:
                tuple = (index, user)
                usersTuple.append(tuple)
                index += 1            
    except: 
        usersTuple = None

    today = datetime.date.today().strftime("%Y-%m-%d")
    
    try:
        obj = Dishplan.objects.get(date=today) 
        dishOfTheDay = Dish.objects.get(pk=obj.dish.id_dish)
    except: dishOfTheDay = None
    
    try: 
        weekday_of_dishType = DishplanSettings.objects.get(pk=datetime.date.today().weekday())
        dishType = DishType.objects.get(pk=weekday_of_dishType.dishType.id_dishType)  
    except:
        dishType = None

    try: 
        bill = Bill.objects.filter(deadlineDate__gte=today).order_by('deadlineDate').first()
    except: bill = None

    template = loader.get_template("home_view.html")
    context = {'users': usersTuple, 'dish': dishOfTheDay, 'dishType': dishType, 'tasks': formset, 'bill': bill}

    return HttpResponse(template.render(request=request, context=context))
