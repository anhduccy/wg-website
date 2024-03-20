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
from app.views import user_view
from app.views import dish_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', user_view.users, name='users'),
    path('dishes/', dish_view.list_view, name = 'dishes'),
    path('dishes/<id_dish>', dish_view.detail_view, name='dishes-detail'),
    path('dishes/add/', dish_view.edit_view, name='dishes-add')
]
