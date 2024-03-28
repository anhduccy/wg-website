from django.db import models
from django import forms
from django.urls import reverse

# Create your models here.

class User(models.Model):
    id_user = models.BigAutoField(primary_key = True)
    name = models.CharField(max_length=45)
    email = models.CharField(max_length=45)
    password = models.CharField(max_length=45)    

    class Meta:
        managed = True
        db_table = 'User'

    def __str__(self):
        return self.name

class DishType(models.Model):
    id_dishType = models.BigAutoField(primary_key = True)
    string = models.CharField(max_length=45)

    class Meta:
        managed = True
        db_table = 'DishType'
    
    def __str__(self):
        return self.string


class Dish(models.Model):
    id_dish = models.BigAutoField(primary_key = True)
    name = models.CharField(max_length=100)
    chef = models.ForeignKey("User", on_delete=models.CASCADE, db_column='chef')
    dishType = models.ForeignKey("DishType", on_delete=models.CASCADE, db_column='dishType')
    proximityDuration = models.IntegerField()
    description = models.CharField(max_length=10000)
    lastTimeEat = models.DateField()

    class Meta:
        managed = True
        db_table = 'Dish'
    
    def get_absolute_url(self):
        return reverse('dishes-detail', args=[self.id_dish])


class Dishplan(models.Model):
    id_dishplan = models.BigAutoField(primary_key=True)
    date = models.DateField()
    dish = models.ForeignKey("Dish", on_delete=models.DO_NOTHING, db_column='dish')

    class Meta:
        managed = True
        db_table = 'Dishplan'

class DishplanSettings(models.Model):
    id_dishplanSettings = models.BigAutoField(primary_key=True)
    weekday = models.CharField(max_length=10)
    dishType = models.ForeignKey("DishType", on_delete=models.DO_NOTHING, db_column='dishType')

    class Meta:
        managed = True
        db_table = 'DishplanSettings'


class Task(models.Model):
    id_task = models.BigAutoField(primary_key = True)
    title = models.CharField(max_length=45)
    #frequency
    responsibility = models.ForeignKey("User", on_delete=models.CASCADE, db_column='responsibility')
    points = models.IntegerField()
    isDone = models.BooleanField()

    class Meta:
        managed = True
        db_table = 'Task'


class TaskEvent(models.Model):
    id_taskEvent = models.BigAutoField(primary_key=True)
    date = models.DateField()
    task = models.ForeignKey("Task", on_delete=models.CASCADE, db_column='task')

    class Meta:
        managed = True
        db_table = 'TaskEvent'

