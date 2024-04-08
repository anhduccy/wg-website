from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader
import datetime
import wg.renderer
import wg.secrets

from app.models import Bill, TransactionBillEntry, Transaction

def createBill(now, deadline, transactions):
    if Transaction.objects.all().count() != 0:
            new_bill = Bill.objects.create(creationDate=now, deadlineDate=deadline)
            for transaction in transactions:
                TransactionBillEntry.objects.create(bill=new_bill, transaction=transaction)

def list_view(request):
    bills = Bill.objects.all()

    now = datetime.datetime.now()
    deadline = datetime.datetime(year=now.year, month=now.month, day=27).strftime("%Y-%m-%d")

    transactions = Transaction.objects.filter(isActive=1)

    try: 
        Bill.objects.filter(deadlineDate=deadline)
    except:
        createBill(now=now, deadline=deadline, transactions=transactions)
    
    if request.method == "POST":
        createBill(now=now, deadline=deadline, transactions=transactions)
        
    context = {'bills': bills}
    template = loader.get_template("bills/bills.html")
    
    return HttpResponse(template.render(request=request, context=context))


def pdf_view(request, id_bill=None):
    transactions = []
    bill = Bill.objects.get(pk=id_bill)
    entries = TransactionBillEntry.objects.filter(bill=id_bill)
    sum = 0 
    for entry in entries:
        transaction = Transaction.objects.get(pk=entry.transaction.id_transaction)
        tuple = (transaction, transaction.sum/3)
        transactions.append(tuple)
        sum += transaction.sum
    
    context = {
        'bill': bill,
        'transactions': transactions,
        'user_info': wg.secrets.UserInfo,
        'sumWG': sum,
        'sum': sum/3
    }
    response = wg.renderer.render_to_pdf("pdf/bill.html", context)

    if response.status_code == 404:
        print("Bill-ERROR")

    return response
