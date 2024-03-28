from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from django.db.models import Count
from datetime import date, timedelta
import random
from app.models import Dish
from app.models import DishType
from app.models import Dishplan
from app.models import DishplanSettings
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
    week = [None] * 7
    dishplan = [None] * 7
    for i in range (0,7):
        date_next = date_today + timedelta(days=i)
        weekday_of_dishType = DishplanSettings.objects.get(pk=date_next.weekday())
        dishType = DishType.objects.get(pk=weekday_of_dishType.dishType.id_dishType)  
        dish = selectDish(dishType=dishType)

        


        dishplan[i] = (weekday_of_dishType.weekday, date_next, dishType, dish) #For HTML rendering
        
    #Configuring the site
    template = loader.get_template("dishplan.html")
    context = {'dishplan': dishplan, 'dishplan_settings': dishplan_settings}

    return HttpResponse(template.render(request=request, context=context))


def selectDish(dishType):
    dishes = Dish.objects.filter(dishType=dishType).order_by('counter')
    if dishes.count() != 0:
        dish_least = dishes.first()
        dishes_least = Dish.objects.filter(dishType=dishType, counter = dish_least.counter) 
        if dishes_least.count() != 0:
            c = random.choice(dishes_least)
            return c


    