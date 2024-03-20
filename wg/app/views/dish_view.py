from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from app.models import Dish
from wg.forms import DishForm

def dish_add_view(request):
    if request.method == "POST":
        form = DishForm(request.POST)
        form.save()
    else:
        form = DishForm()
    context = {'dish_add_view_form': form}
    template = loader.get_template("dish_add_view.html")
    return HttpResponse(template.render(request=request, context=context))

def dish_view(request): 
    dishes = Dish.objects.all()
    context = {'dishes': dishes}
    template = loader.get_template("dish_view.html")
    return HttpResponse(template.render(request=request, context=context))
