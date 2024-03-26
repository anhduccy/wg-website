from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from app.models import User

def foodplan(request):
    template = loader.get_template("foodplan.html")