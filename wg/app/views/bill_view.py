from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader
import datetime

from app.models import Bill, TransactionBillEntry, Transaction

def list_view(request):
    bills = Bill.objects.all()

    now = datetime.datetime.now()
    deadline = datetime.datetime(year=now.year, month=now.month, day=27).strftime("%Y-%m-%d")

    transactions = Transaction.objects.filter(isActive=1)

    try: 
        Bill.objects.get(deadlineDate=deadline)
    except:
        new_bill = Bill.objects.create(creationDate=now, deadlineDate=deadline)
        for transaction in transactions:
            TransactionBillEntry.objects.create(bill=new_bill, transaction=transaction)

    context = {'bills': bills}
    template = loader.get_template("bills/bills.html")
    
    return HttpResponse(template.render(request=request, context=context))