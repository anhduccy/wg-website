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
    template = loader.get_template("dish_add_view.html")
    return HttpResponse(template.render(request=request, context={'dish_add_view_form': form}))