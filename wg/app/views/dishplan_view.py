from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader

from datetime import date, timedelta
import random

from app.models import Dish, DishType, Dishplan, DishplanSettings
from wg.forms import DishplanSettingsForm

def view(request):
    #dishplan_settings -- ERROR
    dishplan_settings = [None] * 7
    for i in range(7):
        weekday_obj = DishplanSettings.objects.get(pk=i)
        weekday = weekday_obj.weekday
        form = DishplanSettingsForm(prefix=i, instance=weekday_obj)

        dishplan_settings[i] = (weekday, form)

        if request.method == 'POST':
            DishplanSettingsForm(request.POST, prefix=i, instance=weekday_obj).save()

    #dishplan
    date_today = date.today()
    dishplan = [None] * 7
    for i in range (0,7):
        date_next = date_today + timedelta(days=i)
        weekday_of_dishType = DishplanSettings.objects.get(pk=date_next.weekday())
        dishType = DishType.objects.get(pk=weekday_of_dishType.dishType.id_dishType)  
        
        try:
            dishplan_obj = Dishplan.objects.get(date=date_next)
        except: 
            dishplan_obj = None

        if dishplan_obj is not None:
            dish = Dish.objects.get(pk=dishplan_obj.dish.id_dish)
        else:
            dish = selectDish(dishType=dishType)
            if dish is not None:    
                dish.lastTimeEat = date_next
                dish.save()
                Dishplan.objects.create(date=date_next, dish=dish)

        dishplan[i] = (weekday_of_dishType.weekday, date_next, dishType, dish) #For HTML rendering
        
    #Configuring the site
    template = loader.get_template("dishplan.html")
    context = {'dishplan': dishplan, 'dishplan_settings': dishplan_settings}

    return HttpResponse(template.render(request=request, context=context))


def selectDish(dishType) -> Dish:
    dishes = Dish.objects.filter(dishType=dishType, lastTimeEat=None)
    if dishes.count() != 0:
        return random.choice(dishes)
    else:
        dishes = Dish.objects.filter(dishType=dishType).order_by('lastTimeEat')
        if dishes.count() != 0:
            dish_oldest = dishes.first()
            dishes = Dish.objects.filter(dishType=dishType, lastTimeEat = dish_oldest.lastTimeEat)
            if dishes.count != 0:
                return random.choice(dishes)
    return None



    