from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader

from app.models import Task
from wg.forms import TaskForm

def list_view(request):
    tasks = Task.objects.all()

    template = loader.get_template("tasks/task_view.html")
    context = {'tasks': tasks}
    return HttpResponse(template.render(request=request, context=context))


def detail_view(request, id_task=None):
    if id_task is not None:
        task = Task.objects.get(pk=id_task)
    else:
        task = None

    form = TaskForm(instance=task)
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if 'save' in request.POST:
            form.save()
        elif 'delete' in request.POST:
            task.delete()
        return redirect('')
    
    template = loader.get_template("task/task_detail_view.html")
    context = {}
    return HttpResponse(template.render(request=request, context=context))