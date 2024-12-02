from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.db.models import Q

from app.models import *
from app.models import Dish
from wg.forms import DishForm, SearchForm

def list_view(request): 
    dishes = Dish.objects.all()

    search_form = SearchForm(request.GET or None)
    if search_form.is_valid():
        query = search_form.cleaned_data.get('query')
        if query:
            dishes = dishes.filter(Q(name__icontains=query))

    context = {'dishes': dishes, 'search_form': search_form}
    template = loader.get_template("dishes/dish_view.html")
    return HttpResponse(template.render(request=request, context=context))


def detail_view(request, id_dish=None):
    if id_dish is not None:
        dish = Dish.objects.get(pk=id_dish)
    else:
        dish = None

    form = DishForm(instance=dish, initial={'chef': User.objects.first().id_user})
    if request.method == "POST":
        form = DishForm(request.POST, instance=dish)
        if 'save' in request.POST:
            form.save()
        elif 'delete' in request.POST:
            dish.delete()
        return redirect('dishes')

    template = loader.get_template("dishes/dish_detail_view.html")
    context = {'dish_edit_form': form}

    return HttpResponse(template.render(request=request, context=context))