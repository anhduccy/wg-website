from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from app.models import User

def users(request):
    users = User.objects.all()
    context = {'users': users}
    template = loader.get_template('user_view.html')
    return HttpResponse(template.render(context=context, request=request))