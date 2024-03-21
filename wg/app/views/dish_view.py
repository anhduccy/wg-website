from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.template import loader
from django.shortcuts import redirect

from app.models import Dish
from wg.forms import DishForm

def list_view(request): 
    dishes = Dish.objects.all()

    context = {'dishes': dishes}
    template = loader.get_template("dishes/dish_view.html")
    return HttpResponse(template.render(request=request, context=context))


def detail_view(request, id_dish=None):
    if id_dish is not None:
        dish = Dish.objects.get(pk=id_dish)
    else:
        dish = None

    form = DishForm()
    if request.method == "POST":
        if 'save' in request.POST:
            form = DishForm(request.POST, instance=dish)
            form.save()
        elif 'delete' in request.POST:
            dish.delete()
        return redirect('dishes')
    else:
        form = DishForm(instance=dish)

    template = loader.get_template("dishes/dish_detail_view.html")
    context = {'dish_edit_form': form}

    return HttpResponse(template.render(request=request, context=context))