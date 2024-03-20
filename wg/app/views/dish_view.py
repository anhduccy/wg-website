from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.template import loader
from django.views.generic.detail import DetailView
from app.models import Dish
from wg.forms import DishForm

def edit_view(request):
    if request.method == "POST":
        form = DishForm(request.POST)
        form.save()
    else:
        form = DishForm()
    context = {'dish_add_form': form}
    template = loader.get_template("dishes/dish_edit_view.html")
    return HttpResponse(template.render(request=request, context=context))

def list_view(request): 
    dishes = Dish.objects.all()

    context = {'dishes': dishes}
    template = loader.get_template("dishes/dish_view.html")
    return HttpResponse(template.render(request=request, context=context))


def detail_view(request, id_dish):
    dish = get_object_or_404(Dish, pk=id_dish)

    if request.method == "POST":
        form = DishForm(request.POST, instance=dish)
        form.save()
    else:
        form = DishForm(instance=dish)

    template = loader.get_template("dishes/dish_detail_view.html")
    context = {'dish_edit_form': form}

    return HttpResponse(template.render(request=request, context=context))