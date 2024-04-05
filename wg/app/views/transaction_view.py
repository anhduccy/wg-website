from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader

def list_view(request):

    context = {}
    template = loader.get_template()
    return HttpResponse(template.render(request=request, context=context))