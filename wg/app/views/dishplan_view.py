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
    #dishplan_settings
    dishplan_settings = [None] * 7
    for i in range(0,7):
        weekday_obj = DishplanSettings.objects.get(pk=i)
        weekday = weekday_obj.weekday
        dishplan_settings[i] = (weekday, DishplanSettingsForm(instance=weekday_obj))

        if request == 'POST':
            dishplan_settings[i] = DishplanSettingsForm(request)
            dishplan_settings[i].save()

    #dishplan
    date_today = date.today()
    week = [None] * 7
    dishplan_header = [None] * 7
    for i in range (0,7):
        date_next = date_today + timedelta(days=i)
        date_dishType = DishplanSettings.objects.get(pk=date_next.weekday())
        dishplan_header[i] = (date_dishType.weekday, date_next)
        dishType = DishType.objects.get(pk=date_dishType.dishType.id_dishType)  
        randomChoice()
        

    template = loader.get_template("dishplan.html")
    context = {'dishplan_header': dishplan_header, 'dishplan_settings': dishplan_settings}

    return HttpResponse(template.render(context=context))


def randomChoice():
    dishes = Dish.objects.all()
    dishType_grouped = Dish.objects.values('dishType').annotate(dcount=Count('dishType')).order_by() #Alle gepseicherten Gerichte gruppiert nach Gerichtsart + Anzahl

    for dishType in dishType_grouped:

        weekday_dishType_counter = DishplanSettings.objects.filter(dishType=dishType.get('dishType')).count() #Anzahl der Wochentage eines Gerichtsartes

        if dishType.get('dcount') < weekday_dishType_counter: #IF Anzahl der Gerichte des Gerichtsartes KLEINER ALS Anzahl der Wochentage, im dem die Gerichtsart vorkommt
            dishes = Dish.objects.filter(pk=dishType.get('dishType'))
            c = choice(dishes)


    