"""
URL configuration for wg project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app.views import user_view, dish_view, dishplan_view, task_view, transaction_view, bill_view, home_view

urlpatterns = [
    #path('admin/', admin.site.urls),
    path('users/', user_view.users, name='users'),

    path('', home_view.view, name='home'),
    
    path('dishplan', dishplan_view.view, name='dishplan'),

    path('dishes/', dish_view.list_view, name = 'dishes'),
    path('dishes/<id_dish>', dish_view.detail_view, name='dishes-detail'),
    path('dishes/add/', dish_view.detail_view, name='dishes-add'),

    path('tasks/', task_view.list_view, name='tasks'),
    path('tasks/<id_task>', task_view.detail_view, name='tasks-detail'),
    path('tasks/add/', task_view.detail_view, name = 'tasks-add'),
    path('tasks/history/', task_view.history_view, name='tasks-history'),

    path('bills/', bill_view.list_view, name='bills'),
    path('bills/pdf/<id_bill>', bill_view.pdf_view, name='bills-detail'),
    path('transactions/', transaction_view.list_view, name='transactions'),
]
