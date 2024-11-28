from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader
from django.forms import modelformset_factory

from app.models import Transaction, TransactionBillEntry, Bill
from wg.forms import TransactionForm

def list_view(request):
    TransactionFormSet = modelformset_factory(model=Transaction, form=TransactionForm)
    formset = TransactionFormSet(queryset=Transaction.objects.filter(isActive=1))

    if request.method == "POST":
        formset = TransactionFormSet(request.POST, queryset=Transaction.objects.order_by('-isEssential').filter(isActive=1))
        if formset.is_valid():
            for form in formset:
                try:
                    if 'save' in request.POST:
                        form.save() 
                    elif 'delete' in request.POST:
                        form.delete(request.POST)
                except: pass

    formset = TransactionFormSet(queryset=Transaction.objects.order_by('-isEssential').filter(isActive=1))

    context = {'formset': formset}
    template = loader.get_template("bills/transactions.html")
    return HttpResponse(template.render(request=request, context=context))