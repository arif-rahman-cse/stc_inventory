import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum, F
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView
from rest_framework.generics import ListAPIView

from setup_data.models import Warehouse
from stock.forms import LcCreateForm, StockCreateForm, StockTransferFrom, WarehouseFrom
from stock.models import LC, Stock, StockTransfer, StockPrime
from stock.serializers import WarehouseSerializer
from rest_framework.response import Response


@login_required
def add_new_lc(request):
    template_name = 'stock/new_lc.html'
    lc_list = LC.objects.all().order_by('-lc_date', '-updated_at')
    warehouse_list = Warehouse.objects.all().order_by('warehouse_name', )

    if request.method == 'GET':
        lc_form = LcCreateForm(request.GET or None)
        warehouse_form = WarehouseFrom(request.GET or None)

    elif request.method == 'POST':
        lc_form = LcCreateForm(request.POST)

        if lc_form.is_valid():
            obj = lc_form.save(commit=False)
            obj.author = request.user
            obj.is_active = True
            obj.save()
            messages.add_message(request, messages.SUCCESS, 'New LC Create Successful!')
            return redirect('new-lc')

        else:
            print("Not Valid Create Form")
            messages.add_message(request, messages.WARNING, 'Lc with this File no, Lc date and Product already exists.')
            print(lc_form.errors)

    return render(request, template_name, {
        'lc_form': lc_form,
        'title': 'New LC',
        'nav_bar': 'new_lc',
        'lcs': lc_list,
        'warehouses': warehouse_list,
        'warehouse_form': warehouse_form,
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
            # obj.type = "Receipt"
            # obj.sign = 1
            obj.is_active = True
            obj.save()

            # Send To StockPrime
            send_to_stock = StockPrime()
            send_to_stock.ref_number = obj.transaction_no
            send_to_stock.stock_in_date = obj.stock_in_date
            send_to_stock.product = obj.product
            send_to_stock.warehouse = obj.warehouse
            send_to_stock.quantity = obj.quantity
            send_to_stock.total_amount_tk = obj.total_amount_tk
            send_to_stock.type = "Receipt"
            send_to_stock.stock_transaction_type = "MNU"
            send_to_stock.sign = 1
            send_to_stock.author = obj.author
            send_to_stock.is_active = True
            send_to_stock.save()

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


class StockedProductListView(LoginRequiredMixin, ListView, ):
    model = Stock  # Model I want to Covert to List
    template_name = 'stock/stocked_product_list.html'  # Template Name
    context_object_name = 'stocks'  # Change default name of objectList
    ordering = ['-stock_in_date', '-updated_at']  # Ordering post LIFO
    paginate_by = 10  # number of page I want to show in single page

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Stocked Product"
        context["nav_bar"] = "stocked_product"
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
            messages.add_message(request, messages.SUCCESS, 'Stock Transfer Request Successfully!')
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
    trans_stock = StockTransfer.objects.get(stock_transfer_no=stock_transfer_no)
    transferable_qty = StockPrime.objects.filter(
        warehouse=trans_stock.from_warehouse, product=trans_stock.product).aggregate(
        total_qty=Sum(F('quantity') * F('sign')))

    trf_able_qty = transferable_qty.get('total_qty')
    trf_qty = trans_stock.transfer_qty

    print("Transferable Qty: " + str(trf_able_qty))
    print("Transfer Qty : " + str(trf_qty))

    if trf_qty <= trf_able_qty:

        # Transfer to stock Issue
        send_to_stock_issue = StockPrime()
        send_to_stock_issue.ref_number = trans_stock.stock_transfer_no
        send_to_stock_issue.stock_in_date = trans_stock.stock_transfer_date
        send_to_stock_issue.product = trans_stock.product
        send_to_stock_issue.warehouse = trans_stock.from_warehouse
        send_to_stock_issue.quantity = trans_stock.transfer_qty
        send_to_stock_issue.total_amount_tk = 0.0
        send_to_stock_issue.type = "Issue"
        send_to_stock_issue.stock_transaction_type = "TRF"
        send_to_stock_issue.sign = -1
        send_to_stock_issue.author = request.user
        send_to_stock_issue.is_active = True
        send_to_stock_issue.save()

        # Transfer to stock Receipt
        send_to_stock_receipt = StockPrime()
        send_to_stock_receipt.ref_number = trans_stock.stock_transfer_no
        send_to_stock_receipt.stock_in_date = trans_stock.stock_transfer_date
        send_to_stock_receipt.product = trans_stock.product
        send_to_stock_receipt.warehouse = trans_stock.to_warehouse
        send_to_stock_receipt.quantity = trans_stock.transfer_qty
        send_to_stock_receipt.total_amount_tk = 0.0
        send_to_stock_receipt.type = "Receipt"
        send_to_stock_receipt.stock_transaction_type = "TRF"
        send_to_stock_receipt.sign = 1
        send_to_stock_receipt.author = request.user
        send_to_stock_receipt.is_active = True
        send_to_stock_receipt.save()

        # Update Transfer  Status
        trans_stock.status = "Transferred"
        trans_stock.save()
        messages.add_message(request, messages.SUCCESS, 'Stock Transfer Successful !')

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
            transferable_qty = StockPrime.objects.filter(warehouse=warehouse_id, product=product_id).aggregate(
                total_qty=Sum(F('quantity') * F('sign')))

            transferable_qty = transferable_qty.get('total_qty')
            if transferable_qty:
                transferable_qty = transferable_qty
            else:
                transferable_qty = 0
        else:
            transferable_qty = 0

        data = {
            "transferable_qty": transferable_qty,
        }
        return JsonResponse(data, status=200)


@login_required
def delete_transfer_stock(request, stock_transfer_no):
    if request.method == 'GET':
        instance = StockTransfer.objects.get(stock_transfer_no=stock_transfer_no)
        instance.delete()
        messages.add_message(request, messages.WARNING, 'Transfer Stick record delete Successful!')
        return redirect('transfer-stock')


@login_required
def new_lc_process(request, lc_transaction_no):
    if request.method == 'GET':
        instance = LC.objects.get(lc_transaction_no=lc_transaction_no)
        instance.status = "Process"
        instance.save()
        messages.add_message(request, messages.WARNING, 'LC Process Successful')
        return redirect('new-lc')


@login_required
def new_lc_closed(request, lc_transaction_no):
    if request.method == 'GET':
        warehouse_name = request.GET.get('warehouse_name', None)
        lc_instance = LC.objects.get(lc_transaction_no=lc_transaction_no)
        print("Warehouse Name")
        print(warehouse_name)
        # Transfer to stock Receipt
        send_to_stock_receipt = StockPrime()
        send_to_stock_receipt.ref_number = lc_instance.lc_transaction_no
        send_to_stock_receipt.stock_in_date = datetime.date.today()
        send_to_stock_receipt.product = lc_instance.product
        send_to_stock_receipt.warehouse = Warehouse.objects.get(id=1)
        send_to_stock_receipt.quantity = lc_instance.quantity
        send_to_stock_receipt.total_amount_tk = lc_instance.total_amount_tk
        send_to_stock_receipt.type = "Receipt"
        send_to_stock_receipt.stock_transaction_type = "LC"
        send_to_stock_receipt.sign = 1
        send_to_stock_receipt.author = request.user
        send_to_stock_receipt.is_active = True
        send_to_stock_receipt.save()

        # Update LC Status
        lc_instance.status = "Closed"
        lc_instance.save()

    messages.add_message(request, messages.SUCCESS, 'LC Closed Successful')
    return redirect('new-lc')


@login_required
def new_lc_delete(request, lc_transaction_no):
    if request.method == 'GET':
        instance = LC.objects.get(lc_transaction_no=lc_transaction_no)
        instance.delete()
        messages.add_message(request, messages.WARNING, 'LC Delete Successful')
        return redirect('new-lc')


@login_required
def get_warehouse_name(request):
    if request.method == "GET" and request.is_ajax():
        print("Get Warehouse Called")
        # Get User ID of specific business
        # access = Profile.objects.get(user=request.user.id).access
        # print(access)
        # # Get Name of user
        warehouses = Warehouse.objects.all()
        print(warehouses)
        serializer = WarehouseSerializer(warehouses, many=True)
        print(serializer.data)
        return Response(serializer.data)
        #
        # data = {
        #     "warehouses": warehouses,
        # }
        # return JsonResponse(data, status=200)


class WarehouseList(LoginRequiredMixin, ListAPIView):
    serializer_class = WarehouseSerializer

    def get_queryset(self):
        print("-------- Warehouse List ---------")
        queryset = Warehouse.objects.all().order_by('warehouse_name', )
        print(queryset)
        return queryset
