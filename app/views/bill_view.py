from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader
import datetime
import wg.renderer
import wg.secrets
import dateutil.relativedelta as dateutil

from app.models import Bill, TransactionBillEntry, Transaction

def list_view(request):
    bills = Bill.objects.all().order_by('-deadlineDate')

    now = datetime.datetime.now()
    deadline = datetime.datetime(year=now.year, month=now.month, day=27).strftime("%Y-%m-%d")

    transactions = Transaction.objects.filter(isActive=1)
    
    if request.method == "POST":
        createBill(now=now, deadline=deadline, transactions=transactions)
        
    context = {'bills': bills, 'last_bill': bills.first}
    template = loader.get_template("bills/bills.html")
    
    return HttpResponse(template.render(request=request, context=context))

def pdf_view(request, id_bill=None):
    transactions = []
    
    #SUM THIS MONTH
    bill = Bill.objects.get(pk=id_bill)
    entries = TransactionBillEntry.objects.filter(bill=id_bill)
    sum = 0
    sum_notCommunal = 0
    for entry in entries:
        transaction = Transaction.objects.get(pk=entry.transaction.id_transaction)
        tuple = (transaction, transaction.sum/3)
        transactions.append(tuple)
        if transaction.isEssential: 
            sum_notCommunal += transaction.sum
        sum += transaction.sum

    #SUM LAST MONTH
    bill_last_month = Bill.objects.filter(deadlineDate__lt=bill.deadlineDate).last()
    sum_last_month = 0 
    sum_last_month_notCommunal = 0
    if(bill_last_month != None): 
        entries_last_month = TransactionBillEntry.objects.filter(bill=bill_last_month.id_bill)
        for entry in entries_last_month:
            transaction = Transaction.objects.get(pk=entry.transaction.id_transaction)
            if transaction.isEssential: 
                sum_last_month_notCommunal += transaction.sum
            sum_last_month += transaction.sum
    
    context = {
        'bill': bill,
        'transactions': transactions,
        'user_info': wg.secrets.UserInfo,
        'sumWG': sum,
        'sumWG_notCommunal': sum_notCommunal,
        'sum': sum/3,
        'sum_notCommunal': sum_notCommunal/3,
        'sumWG_last_month': sum - sum_last_month if sum_last_month > 0 else 0,
        'sumWG_last_month_notCommunal': sum_notCommunal - sum_last_month_notCommunal if sum_last_month_notCommunal > 0 else 0,
        'sum_last_month': sum/3 - sum_last_month/3 if sum_last_month/3 > 0 else 0,
        'sum_last_month_notCommunal': sum_notCommunal/3 - sum_last_month_notCommunal/3 if sum_last_month_notCommunal/3 > 0 else 0,
        'next_date': bill.deadlineDate + dateutil.relativedelta(months=1)
    }
    response = wg.renderer.render_to_pdf("pdf/bill.html", context)

    if response.status_code == 404:
        print("Bill-ERROR")

    return response

def createBill(now, deadline, transactions):
    if Transaction.objects.all().count() != 0:
            new_bill = Bill.objects.create(creationDate=now, deadlineDate=deadline)
            for transaction in transactions:
                TransactionBillEntry.objects.create(bill=new_bill, transaction=transaction)
