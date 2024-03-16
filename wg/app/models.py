from django.db import models
from django import forms

# Create your models here.

class User(models.Model):
    id_user = models.BigAutoField(primary_key = True)
    name = models.CharField(max_length=45)
    email = models.CharField(max_length=45)
    password = models.CharField(max_length=45)    

    class Meta:
        managed = True
        db_table = 'User'


class Dish(models.Model):
    id_dish = models.BigAutoField(primary_key = True)
    name = models.CharField(max_length=100)
    proximityDuration = models.IntegerField()
    description = models.CharField(max_length=10000)

    class Meta:
        managed = True
        db_table = 'Dish'