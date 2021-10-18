from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum, F
from django.http import JsonResponse
from django.shortcuts import render, redirect
# Create your views here.
from django.views.generic import ListView

from stock.forms import LcCreateForm, StockCreateForm, StockTransferFrom
from stock.models import LC, Stock, StockTransfer


@login_required
def add_new_lc(request):
    template_name = 'stock/new_lc.html'
    lc_list = LC.objects.all().order_by('-date', '-updated_at')

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


@login_required
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
            return redirect('stock-in-list')

        else:
            print("Not Valid Create Form")
            print(stock_form.errors)

    return render(request, template_name, {
        'stock_form': stock_form,
        'title': 'Add Stock',
        'nav_bar': 'add_stock',
    })


class StockInListView(LoginRequiredMixin, ListView, ):
    model = Stock  # Model I want to Covert to List
    template_name = 'stock/stock_in_list.html'  # Template Name
    context_object_name = 'stocks'  # Change default name of objectList
    ordering = ['-stock_in_date', '-updated_at']  # Ordering post LIFO
    paginate_by = 10  # number of page I want to show in single page

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Stock In List"
        context["nav_bar"] = "stock_in_list"
        context['stock_list'] = self.model.objects.all()
        return context


@login_required
def transfer_stock(request):
    transfer_stock_list = StockTransfer.objects.all().order_by('-stock_transfer_date', '-updated_at')
    template_name = 'stock/transfer_stock.html'
    if request.method == 'GET':
        stock_transfer_form = StockTransferFrom(request.GET or None)

    elif request.method == 'POST':
        stock_transfer_form = StockTransferFrom(request.POST)
        if stock_transfer_form.is_valid():
            obj = stock_transfer_form.save(commit=False)
            obj.author = request.user
            obj.status = "Open"
            obj.is_active = True
            obj.save()
            messages.add_message(request, messages.SUCCESS, 'Stock Transfer Successfully!')
            return redirect('transfer-stock')

        else:
            print("Not Valid Create Form")
            print(stock_transfer_form.errors)

    return render(request, template_name, {
        'stock_transfer_form': stock_transfer_form,
        'title': 'Transfer Stock',
        'nav_bar': 'transfer_stock',
        'transfer_stocks': transfer_stock_list,
    })


@login_required
def transfer_stock_confirm(request, stock_transfer_no):
    print("transfer_stock_confirm called")
    print("stock_transfer_no: " + stock_transfer_no)
    stock = StockTransfer.objects.get(stock_transfer_no=stock_transfer_no)
    transferable_qty = Stock.objects.filter(warehouse=stock.from_warehouse, product=stock.product).aggregate(
        total_qty=Sum(F('quantity') * F('sign')))

    trf_able_qty = transferable_qty.get('total_qty')
    trf_qty = stock.transfer_qty

    print("Transferable Qty: " + str(trf_able_qty))
    print("Transfer Qty : " + str(trf_qty))

    if trf_qty <= trf_able_qty:

        # trans_stock = Stock()
        # trans_stock.ref_number = stock.stock_transfer_no
        # trans_stock.contents = stock.stock_transfer_date
        # trans_stock.contents = stock.product
        # trans_stock.contents = stock.product
        # trans_stock.save()
        pass

    else:
        messages.add_message(request, messages.WARNING, 'Insufficient stock! Transferable Stock: ' + str(trf_able_qty))

    return redirect('transfer-stock')


@login_required
def transferable_stock_qty(request):
    print("transferable_stock_qty called")
    if request.method == "GET" and request.is_ajax():
        product_id = request.GET['product_id']
        warehouse_id = request.GET['warehouse_id']
        print(product_id)
        print(warehouse_id)

        if product_id and warehouse_id:
            transferable_qty = Stock.objects.filter(warehouse=warehouse_id, product=product_id).aggregate(
                total_qty=Sum(F('quantity') * F('sign')))
            print("Total Qty")
            print(transferable_qty)
            transferable_qty = transferable_qty.get('total_qty')
        else:
            transferable_qty = 0

        data = {
            "transferable_qty": transferable_qty,
        }
        return JsonResponse(data, status=200)
