from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum, F
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.views.generic.base import View
from sales.forms import SalesCreateForm, SalesChildFormset
from sales.models import SalesParent, SalesChild
from sales.serializers import SalesItemSerializerPopUp
from sales.utils import render_to_pdf, getWords
from setup_data.models import Customers
from stock.models import StockPrime
from django.db import IntegrityError


class SalesListView(LoginRequiredMixin, ListView, ):
    model = SalesParent  # Model I want to Covert to List
    template_name = 'sales/sales.html'  # Template Name
    context_object_name = 'sales'  # Change default name of objectList
    ordering = ['-order_date', '-updated_at']  # Ordering post LIFO
    paginate_by = 20  # number of page I want to show in single page

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Sales List"
        context["nav_bar"] = "sales"
        context['stocks_list'] = self.model.objects.all()
        return context


@login_required
def new_sales(request):
    template_name = 'sales/new_sales.html'

    if request.method == 'GET':
        print("GET called")
        sales_form = SalesCreateForm(None)
        sales_form_child = SalesChildFormset(queryset=SalesChild.objects.none())

    elif request.method == 'POST':
        print("Post called")
        sales_form = SalesCreateForm(request.POST)
        sales_form_child = SalesChildFormset(request.POST)

        if sales_form.is_valid() and sales_form_child.is_valid():
            sales_parent = sales_form.save(commit=False)
            sales_parent.author = request.user
            sales_parent.is_active = True
            sales_parent.save()

            for form in sales_form_child:

                if form.is_valid():
                    try:
                        child = form.save(commit=False)
                        child.order_date = sales_parent.order_date
                        # child.invoice_no = sales_parent.invoice_no
                        child.invoice_no = SalesParent.objects.get(invoice_no=sales_parent.invoice_no)
                        child.author = sales_parent.author
                        child.is_active = True
                        child.save()
                    except IntegrityError as e:
                        if 'unique constraint' in e.args:
                            messages.add_message(request, messages.SUCCESS, 'You are entering the same item multiple times')
                            return
                else:
                    print("Child Form Error")
                    print(form.errors)

            messages.add_message(request, messages.SUCCESS, 'New Sales Entry Successful')
            return redirect('sales-list')

        else:
            print("Not Valid Create Form")
            print(sales_form.errors)
            print(sales_form_child.errors)

    return render(request, template_name, {
        'sales_form': sales_form,
        'formset': sales_form_child,
        'title': 'New Sales',
        'nav_bar': 'new_sales',
    })


@login_required
def sales_post(request, invoice_no):
    print("invoice_no: " + invoice_no)
    sales_request_parent = SalesParent.objects.get(invoice_no=invoice_no)

    sales_request_child = SalesChild.objects.filter(invoice_no=sales_request_parent.invoice_no)

    for child in sales_request_child:
        stock_obj = StockPrime()
        stock_obj.ref_number = child.invoice_no
        stock_obj.stock_in_date = datetime.today().strftime('%Y-%m-%d')
        stock_obj.product = child.product
        stock_obj.warehouse = sales_request_parent.warehouse
        stock_obj.quantity = child.quantity
        stock_obj.total_amount_tk = 0.0
        stock_obj.type = "Issue"
        stock_obj.stock_transaction_type = "SALE"
        stock_obj.sign = -1
        stock_obj.author = request.user
        stock_obj.is_active = True
        stock_obj.save()

    sales_request_parent.status = "Post"
    sales_request_parent.save()

    messages.add_message(request, messages.SUCCESS, 'Stock Posted Successfully !')

    return redirect('sales-list')


@login_required
def sales_delete(request, invoice_no):
    if request.method == 'GET':
        instance = SalesParent.objects.get(invoice_no=invoice_no)
        SalesChild.objects.filter(invoice_no=instance.invoice_no).delete()
        instance.delete()
        messages.add_message(request, messages.WARNING, 'Delete Success')
        return redirect('sales-list')


@login_required
def print_challan(request, invoice_no):
    print(invoice_no)
    sales_parent = SalesParent.objects.get(invoice_no=invoice_no)
    sales_child = SalesChild.objects.filter(invoice_no=invoice_no)
    total_qty = sales_child.aggregate(Sum('quantity'))
    total_qty = total_qty.get('quantity__sum')
    print(total_qty)

    # print('%d in words is: %s' % (total_amount, getWords(total_amount)))

    context = {
        'title': "Daily Attendants Sheet",
        'nav_bar': "report_nav",
        'sales_item': sales_child,
        'total_qty': total_qty,
        'challan_info': sales_parent,
    }
    pdf = render_to_pdf('sales/challan_print.html', context)
    return HttpResponse(pdf, content_type='application/pdf')
    # return render(request, template_name, context)


@login_required
def print_bill(request, invoice_no):
    print(invoice_no)
    sales_parent = SalesParent.objects.get(invoice_no=invoice_no)
    sales_child = SalesChild.objects.filter(invoice_no=invoice_no)
    total_amount = sales_child.aggregate(Sum('amount'))
    total_amount = total_amount.get('amount__sum')
    print(total_amount)

    # print('%d in words is: %s' % (total_amount, getWords(total_amount)))

    context = {
        'title': "Daily Attendants Sheet",
        'nav_bar': "report_nav",
        'sales_item': sales_child,
        'total_tk': total_amount,
        'challan_info': sales_parent,
        'total_taka_word': getWords(total_amount)
    }
    pdf = render_to_pdf('sales/bill_print.html', context)
    return HttpResponse(pdf, content_type='application/pdf')
    # return render(request, template_name, context)


class GeneratePdf(View):
    def get(self, request, *args, **kwargs):
        # getting the template
        pdf = render_to_pdf('sales/bill_print.html')

        # rendering the template
        return HttpResponse(pdf, content_type='application/pdf')


@login_required
def customer_info(request):
    print("customer_info called")
    customer_code = request.GET.get('customer_code', None)
    customer = Customers.objects.get(customer_code=customer_code)
    data = {
        'address': customer.customer_address,
        'phone': customer.phone,
    }
    # print(data)
    return JsonResponse(data, status=200)


@login_required
def stock_by_warehouse(request):
    print("warehouse stock  called")
    warehouse_id = request.GET.get('warehouse_id', None)
    item = request.GET.get('item', None)

    available_qty = StockPrime.objects.filter(warehouse=warehouse_id, product=item).aggregate(
        total_qty=Sum(F('quantity') * F('sign')))
    available_qty = available_qty.get('total_qty')
    if available_qty is None:
        available_qty = 0.0
    data = {
        'stock': available_qty,
    }
    # print(data)
    return JsonResponse(data, status=200)


def sales_item_popup(request):
    invoice_no = request.GET['invoice_no']
    dataset = SalesChild.objects.filter(invoice_no=invoice_no)
    list_1 = list()
    for item in dataset:
        ser = SalesItemSerializerPopUp(item)
        list_1.append(ser.data)
    return JsonResponse(list_1, safe=False)
