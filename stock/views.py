from django.contrib import messages
from django.shortcuts import render, redirect

# Create your views here.
from django.views.generic import CreateView, ListView

from stock.forms import LcCreateForm, StockCreateForm
from stock.models import LC, Stock


def stock(request):
    context = {'title': 'Stock List',
               'nav_bar': 'stock_ledger',
               }
    return render(request, 'stock/stock_ledger.html', context)


def add_new_lc(request):
    template_name = 'stock/new_lc.html'
    lc_list = LC.objects.all().order_by('updated_at')
    if request.method == 'GET':
        lc_form = LcCreateForm(request.GET or None)

    elif request.method == 'POST':
        lc_form = LcCreateForm(request.POST)

        if lc_form.is_valid():
            obj = lc_form.save(commit=False)
            obj.author = request.user
            obj.is_active = True
            obj.save()
            messages.add_message(request, messages.SUCCESS, 'New Product Added Successfully!')
            return redirect('new-lc')

        else:
            print("Not Valid Create Form")
            print(lc_form.errors)

    return render(request, template_name, {
        'lc_form': lc_form,
        'title': 'New LC',
        'nav_bar': 'new_lc',
        'lcs': lc_list,
    })


def add_stock(request):
    template_name = 'stock/add_new_stock.html'

    if request.method == 'GET':
        stock_form = StockCreateForm(request.GET or None)

    elif request.method == 'POST':
        stock_form = StockCreateForm(request.POST)

        if stock_form.is_valid():
            obj = stock_form.save(commit=False)
            obj.author = request.user
            obj.type = "Receipt"
            obj.sign = 1
            obj.is_active = True
            obj.save()
            messages.add_message(request, messages.SUCCESS, 'New Stock Added Successfully!')
            return redirect('stock-ledger')

        else:
            print("Not Valid Create Form")
            print(stock_form.errors)

    return render(request, template_name, {
        'stock_form': stock_form,
        'title': 'Add Stock',
        'nav_bar': 'add_stock',
    })


class StockLedgerListView(ListView, ):
    model = Stock  # Model I want to Covert to List
    template_name = 'stock/stock_ledger.html'  # Template Name
    context_object_name = 'stocks'  # Change default name of objectList
    ordering = ['-updated_at']  # Ordering post LIFO
    paginate_by = 20  # number of page I want to show in single page

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Stock List"
        context["nav_bar"] = "stock_ledger"
        context['products'] = Stock.objects.all().order_by('-updated_at')
        return context
