from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from app.models import User

def dishplan(request):
    template = loader.get_template("foodplan.html")
    return render(template=template)