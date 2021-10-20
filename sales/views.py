from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import JsonResponse
# Create your views here.
from sales.forms import SalesCreateForm, SalesChildFormCreateForm, SalesChildFormset
from setup_data.models import Customers


def sales(request):
    template_name = 'sales/sales.html'

    return render(request, template_name, {
        'title': 'Sales List',
        'nav_bar': 'sales',
    })


def new_sales(request):
    if request.method == 'GET':
        sales_form = SalesCreateForm(request.GET or None)
        sales_form_child = SalesChildFormset(request.GET or None)

    elif request.method == 'POST':
        sales_form = SalesCreateForm(request.POST)
        sales_form_child = SalesChildFormset(request.POST)

        if sales_form.is_valid():
            # obj = stock_form.save(commit=False)
            # obj.author = request.user
            # # obj.type = "Receipt"
            # # obj.sign = 1
            # obj.is_active = True
            # obj.save()
            #
            # # Send To StockPrime
            # send_to_stock = StockPrime()
            # send_to_stock.ref_number = obj.transaction_no
            # send_to_stock.stock_in_date = obj.stock_in_date
            # send_to_stock.product = obj.product
            # send_to_stock.warehouse = obj.warehouse
            # send_to_stock.quantity = obj.quantity
            # send_to_stock.total_amount_tk = obj.total_amount_tk
            # send_to_stock.type = "Receipt"
            # send_to_stock.stock_transaction_type = "MNU"
            # send_to_stock.sign = 1
            # send_to_stock.author = obj.author
            # send_to_stock.is_active = True
            # send_to_stock.save()

            messages.add_message(request, messages.SUCCESS, 'New Stock Added Successfully!')
            return redirect('stock-in-list')

        else:
            print("Not Valid Create Form")
            print(sales_form.errors)
    template_name = 'sales/new_sales.html'

    return render(request, template_name, {
        'sales_form': sales_form,
        'formset': sales_form_child,
        'title': 'New Sales',
        'nav_bar': 'new_sales',
    })


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
