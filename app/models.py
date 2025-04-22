from django.db import models
from django.urls import reverse
import datetime


class User(models.Model):
    id_user = models.BigAutoField(primary_key = True)
    name = models.CharField(max_length=45)
    email = models.CharField(max_length=45)
    password = models.CharField(max_length=45)    
    points = models.IntegerField()
    isCommunal = models.BooleanField(default=1)

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
    frequency = models.IntegerField()
    creationDate = models.DateTimeField(default=datetime.datetime.today)
    lastChangeDate = models.DateTimeField(default=datetime.datetime.today)
    deadlineDate = models.DateField(default=datetime.date.today)
    responsibility = models.ForeignKey("User", on_delete=models.CASCADE, db_column='responsibility')
    points = models.IntegerField()
    isDone = models.BooleanField(default=0)

    class Meta:
        managed = True
        db_table = 'Task'

    def get_absolute_url(self):
        return reverse('tasks-detail', args=[self.id_task])
    

class TaskLogEvent(models.Model):
    id_taskLogEvent = models.BigAutoField(primary_key=True)
    event = models.CharField(max_length=500)
    task = models.ForeignKey('Task', on_delete=models.CASCADE, db_column="task")
    eventDate = models.DateTimeField(default=datetime.datetime.now)
    ipAddress = models.CharField(max_length=20)

    class Meta:
        managed = True
        db_table = 'TaskLogEvent'


class Transaction(models.Model):
    id_transaction = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=45)
    sum = models.DecimalField(decimal_places=2, max_digits=6)
    isActive = models.BooleanField(default = 1)
    isEssential = models.BooleanField(default = 0)

    class Meta:
        managed = True
        db_table = 'Transaction'


class Bill(models.Model):
    id_bill = models.BigAutoField(primary_key=True)
    creationDate = models.DateTimeField(default=datetime.datetime.today)
    deadlineDate = models.DateField(default=datetime.date.today)

    class Meta:
        managed=True
        db_table= 'Bill'
            
    def get_absolute_url(self):
        return reverse('bills-detail', args=[self.id_bill])
    

class TransactionBillEntry(models.Model):
    id_transactionBillEntry = models.BigAutoField(primary_key=True)
    bill = models.ForeignKey("Bill", on_delete=models.CASCADE, db_column='bill')
    transaction = models.ForeignKey("Transaction", on_delete=models.CASCADE, db_column='transaction')

    class Meta:
        managed=True
        db_table = 'TransactionBillEntry'


class IP(models.Model):
    id_IP = models.CharField(primary_key=True, max_length=20, unique=True)
    user = models.ForeignKey("User", on_delete=models.CASCADE, db_column='user')

    class Meta:
        managed=True
        db_table = 'IP'
