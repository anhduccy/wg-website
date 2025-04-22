from django.http import HttpResponse
from django.template import loader
import datetime
import wg.renderer
import wg.secrets
import dateutil.relativedelta as dateutil

from app.models import Bill, TransactionBillEntry, Transaction, User

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
    context = {'user_info': wg.secrets.UserInfo}

    bill: Bill = Bill.objects.get(pk=id_bill)
    if bill is not None:
        result = sumForBill(id_bill=bill.id_bill) 
        context.update({
            'bill': bill,
            'transactions': result[0], #transactions
            'sumWG': result[1], #sum
            'sumWG_notCommunal': result[2], #sum_notCommunal
            'sum': result[3], #sum_communal_per_user
            'sum_notCommunal': result[4], #sum_notCommunal_per_user
            'next_date': bill.deadlineDate + dateutil.relativedelta(months=1)
        })

    bill_last_month: Bill = Bill.objects.filter(deadlineDate__lt=bill.deadlineDate).last()
    if bill_last_month is not None:
        result_last_month = sumForBill(id_bill=bill_last_month.id_bill)
        context.update({
            'sumWG_last_month': result[1] - result_last_month[1] if result_last_month[1] > 0 else 0,
            'sumWG_last_month_notCommunal': result[2] - result_last_month[2] if result_last_month[2] > 0 else 0,
            'sum_last_month': result[3] - result_last_month[3] if result_last_month[3] > 0 else 0,
            'sum_last_month_notCommunal': result[4] - result_last_month[4] if result_last_month[4] > 0 else 0,
        })
    
    response = wg.renderer.render_to_pdf("pdf/bill.html", context)

    if response.status_code == 404:
        print("Bill-ERROR")

    return response


#---FUNCTIONS---#
def sumForBill(id_bill):
    transactions: list[tuple[Transaction, float]] = []
    entries: list[TransactionBillEntry] = TransactionBillEntry.objects.filter(bill=id_bill)
    users_amount: int = User.objects.all().count()
    users_amount_communal: int = User.objects.filter(isCommunal=1).count()
    if users_amount_communal == 0: users_amount_communal = users_amount
    sum_communal: float = 0
    sum_communal_per_user: float = 0
    sum_notCommunal: float = 0
    sum_notCommunal_per_user: float = 0
    for entry in entries:
        transaction = Transaction.objects.get(pk=entry.transaction.id_transaction)
        if transaction.isEssential:
            result_tuple: tuple[Transaction, float] = (transaction, transaction.sum/users_amount)
            sum_communal += transaction.sum
            sum_notCommunal += transaction.sum
            sum_communal_per_user += transaction.sum/users_amount
            sum_notCommunal_per_user += transaction.sum/users_amount
        else: #isCommunal
            result_tuple: tuple[Transaction, float] = (transaction, transaction.sum/users_amount_communal)
            sum_communal += transaction.sum
            sum_communal_per_user += transaction.sum/users_amount_communal
        transactions.append(result_tuple)
    
    return transactions, sum_communal, sum_notCommunal, sum_communal_per_user, sum_notCommunal_per_user

def createBill(now, deadline, transactions):
    if Transaction.objects.all().count() != 0:
            new_bill = Bill.objects.create(creationDate=now, deadlineDate=deadline)
            for transaction in transactions:
                TransactionBillEntry.objects.create(bill=new_bill, transaction=transaction)
