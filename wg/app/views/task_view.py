from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader

from app.models import Task
from wg.forms import TaskForm, TaskCheckboxForm

def list_view(request):
    #list_view
    tasks = []
    for task in Task.objects.all():
        task_checkbox_form = TaskCheckboxForm(instance=task)
        task_tuple = (task_checkbox_form, task)
        tasks.append(task_tuple)

        if request.method == "POST":
            task_checkbox_form = TaskCheckboxForm(request.POST, instance=task)
            print(task_checkbox_form)
            task_checkbox_form.save()

    context = {'tasks': tasks}
    template = loader.get_template("tasks/task_view.html")
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
        return redirect('tasks')
    
    template = loader.get_template("tasks/task_detail_view.html")
    context = {'task_edit_form': form}
    return HttpResponse(template.render(request=request, context=context))