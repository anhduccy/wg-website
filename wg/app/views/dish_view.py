from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.template import loader
from django.views.generic.detail import DetailView
from app.models import Dish
from wg.forms import DishForm

def add_view(request):
    if request.method == "POST":
        form = DishForm(request.POST)
        form.save()
    else:
        form = DishForm()
    context = {'dish_add_view_form': form}
    template = loader.get_template("dish_add_view.html")
    return HttpResponse(template.render(request=request, context=context))

def list_view(request): 
    dishes = Dish.objects.all()

    context = {'dishes': dishes}
    template = loader.get_template("dish_view.html")
    return HttpResponse(template.render(request=request, context=context))

class DishDetailView(DetailView):
    model = Dish
    template_name = "dish_detail_view.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

def detail_view(request, id_dish):
    dish = get_object_or_404(Dish, pk=id_dish)

    template = loader.get_template("dish_detail_view.html")
    context = {'dish': dish}

    return HttpResponse(template.render(request=request, context=context))