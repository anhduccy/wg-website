from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader
from django.forms import modelformset_factory

from app.models import Task, User
from wg.forms import TaskAddForm, TaskEditForm, TaskCheckboxForm


def list_view(request):    
    TaskFormSet = modelformset_factory(model=Task, form=TaskCheckboxForm, extra=0, fields = ('isDone',))
    formset = TaskFormSet()

    if request.method == "POST":
        formset = TaskFormSet(request.POST)
        if formset.is_valid():
            for form in formset:
                form.save()

    formset = TaskFormSet()

    context = {'formset': formset}
    template = loader.get_template("tasks/task_view.html")
    return HttpResponse(template.render(request=request, context=context))


def detail_view(request, id_task=None):
    if id_task is None:
        form = TaskAddForm(initial={'responsibility': TaskCheckboxForm.getNextResponsibility().id_user}, instance=None) 
    else:
        task = Task.objects.get(pk=id_task)
        form = TaskEditForm(instance=task)

    if request.method == "POST":
        if id_task is None:
            form = TaskAddForm(request.POST, instance=None)
        else:
            form = TaskEditForm(request.POST, instance=task)
        if 'save' in request.POST:
            new_task = form.save()
        elif 'delete' in request.POST:
            task.delete()
        return redirect('tasks')
    
    template = loader.get_template("tasks/task_detail_view.html")
    context = {'task_edit_form': form}
    return HttpResponse(template.render(request=request, context=context))

def history_view(request):
    tasks = Task.objects.filter(isDone=1).order_by('-lastChangeDate')

    context = {'tasks': tasks}
    template = loader.get_template("tasks/task_history_view.html")
    return HttpResponse(template.render(request=request, context=context))