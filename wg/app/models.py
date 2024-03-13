from django.db import models
from django import forms

# Create your models here.

class User(models.Model):
    id_user = models.CharField(max_length=45, primary_key=True)
    name = models.CharField(max_length=45)
    email = models.CharField(max_length=45)
    password = models.CharField(max_length=45)    

    class Meta:
        managed = True
        db_table = 'User'