from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader
from django.forms import modelformset_factory
from django.db.models import Q, Case, Value, When
from django.core.paginator import Paginator

from app.models import Task, TaskLogEvent, IP, User
from wg.forms import TaskAddForm, TaskEditForm, TaskCheckboxForm, SearchForm
import datetime

from app.task_log_event import *
from app.functions import *

def list_view(request):
    tasks = Task.objects.filter(isDone=0).annotate(custom_order=Case(When(frequency="-1", then=Value(1)), default=Value(0))).order_by('custom_order','deadlineDate')

    search_form = SearchForm(request.GET or None)
    if search_form.is_valid():
        query = search_form.cleaned_data.get('query')
        if query:
            tasks = tasks.filter(Q(title__icontains=query))

    TaskFormSet = modelformset_factory(model=Task, form=TaskCheckboxForm, extra=0, fields = ('isDone',))
    formset = TaskFormSet(queryset=tasks)

    if request.method == "POST":
        formset = TaskFormSet(request.POST, queryset=tasks)
        if formset.is_valid():
            for form in formset:
                form.save(request)
        return redirect('tasks')

    formset = TaskFormSet(queryset=tasks)

    context = {'formset': formset, 'search_form': search_form}
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
            new_task = form.save(request=request)
        elif 'delete' in request.POST:
            task.isDone = 1
            task.lastChangeDate = datetime.datetime.now()
            task.save()
            TaskLogEvent.objects.create(event=TaskLogEventDescription.delete.value, task=task, ipAddress=getIP(request))
            
        return redirect('tasks')
    
    template = loader.get_template("tasks/task_detail_view.html")
    context = {'task_edit_form': form}
    return HttpResponse(template.render(request=request, context=context))

def history_view(request):
    tasks = TaskLogEvent.objects
    search_form = SearchForm(request.GET or None)
    if search_form.is_valid():
        query = search_form.cleaned_data.get('query')
        if query:
            tasks = tasks.filter(Q(task__title__icontains=query))

    tasks = tasks.order_by('-eventDate', '-task_id')[0:74]

    tasks_t = []
    for task in tasks:
        try:
            task_t = [task,  IP.objects.get(pk=task.ipAddress).user.name]
        except: task_t = [task, task.ipAddress]
        tasks_t.append(task_t)
    
    page_number = request.GET.get('page', 1)
    tasks_t = Paginator(tasks_t, 15).get_page(page_number) 

    context = {'tasks': tasks_t, 'search_form': search_form}
    template = loader.get_template("tasks/task_history_view.html")
    return HttpResponse(template.render(request=request, context=context))
