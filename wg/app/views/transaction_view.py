from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader
from django.forms import modelformset_factory

from app.models import Transaction, TransactionBillEntry, Bill
from wg.forms import TransactionForm

def list_view(request):
    TransactionFormSet = modelformset_factory(model=Transaction, form=TransactionForm, fields = ('title', 'sum'))
    formset = TransactionFormSet()

    if request.method == "POST":
        formset = TransactionFormSet(request.POST)
        if formset.is_valid():
            for form in formset:
                try:
                    if 'save' in request.POST:
                        form.save() 
                    elif 'delete' in request.POST:
                        form.delete(request.POST)
                except: pass

    formset = TransactionFormSet()

    context = {'formset': formset}
    template = loader.get_template("bills/transactions.html")
    return HttpResponse(template.render(request=request, context=context))