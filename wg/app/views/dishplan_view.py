from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from django.db.models import Count
from datetime import date, timedelta
from random import *
from app.models import Dish
from app.models import DishType
from app.models import DishplanSettings
from wg.forms import DishplanSettingsForm

def view(request):
    date_today = date.today()
    week = [None] * 7
    forms = [None] * 7
    for i in range (0,7):
        date_next = date_today + timedelta(days=i)
        date_dishType = DishplanSettings.objects.get(pk=date_next.weekday())
        forms[i] = (date_dishType.weekday, date_next , DishplanSettingsForm(instance=date_dishType))
        dishType = DishType.objects.get(pk=date_dishType.dishType.id_dishType)  
    randomChoice()

    if request == 'POST':
        form = DishplanSettingsForm(request)
        form.save()
        

    template = loader.get_template("dishplan.html")
    context = {'weekday_dishType_forms': forms}

    return HttpResponse(template.render(context=context))


def randomChoice():
    dishes = Dish.objects.all()
    dishType_grouped = Dish.objects.values('dishType').annotate(dcount=Count('dishType')).order_by() #Alle gepseicherten Gerichte gruppiert nach Gerichtsart + Anzahl

    for dishType in dishType_grouped:

        weekday_dishType_counter = DishplanSettings.objects.filter(dishType=dishType.get('dishType')).count() #Anzahl der Wochentage eines Gerichtsartes

        if dishType.get('dcount') < weekday_dishType_counter: #IF Anzahl der Gerichte des Gerichtsartes KLEINER ALS Anzahl der Wochentage, im dem die Gerichtsart vorkommt
            dishes = Dish.objects.filter(pk=dishType.get('dishType'))
            c = choice(dishes)
            print(c.name)
        else:
            print('False')

    