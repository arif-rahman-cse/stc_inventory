from django.contrib import messages
from django.shortcuts import render, redirect
from .models import Customers, Products, Category, Origin
from .forms import CustomerCreateForm, ProductsCreateForm

from django.views.generic import (
    CreateView,
    UpdateView,
    DeleteView,
    DetailView,
    ListView,
    TemplateView)


def all_products(request):
    context = {'title': 'Product List',
               'nav_bar': 'product_list',
               }
    return render(request, 'product/products.html', context)


class AllProductsListView(ListView, ):
    model = Products  # Model I want to Covert to List
    template_name = 'product/products.html'  # Template Name
    context_object_name = 'products'  # Change default name of objectList
    ordering = ['-updated_at']  # Ordering post LIFO
    paginate_by = 20  # number of page I want to show in single page

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Product List"
        context["nav_bar"] = "product_list"
        context['products'] = Products.objects.all().order_by('-updated_at')
        print(context)
        return context


def add_new_product(request):
    template_name = 'product/add_new_product.html'

    if request.method == 'GET':
        product_form = ProductsCreateForm(request.GET or None)

    elif request.method == 'POST':
        print(request.POST)
        product_form = ProductsCreateForm(request.POST)

        if product_form.is_valid():
            obj = product_form.save(commit=False)
            obj.author = request.user
            obj.is_active = True
            obj.save()
            messages.add_message(request, messages.SUCCESS, 'New Product Added Successfully!')
            return redirect('all-products')

        else:
            print("Not Valid Create Form")
            print(product_form.errors)

    return render(request, template_name, {
        'product_form': product_form,
        'title': 'Add New Product',
        'nav_bar': 'add_new_product',
    })


# def add_new_product(request):
#     context = {'title': 'Add New Product',
#                'nav_bar': 'add_new_product',
#                }
#     return render(request, 'product/add_new_product.html', context)


# def all_customers(request):
#     context = {'title': 'Customer List',
#                'nav_bar': 'customer_list',
#                }
#     return render(request, 'customer/customers.html', context)

class AllCustomerListView(ListView, ):
    model = Customers  # Model I want to Covert to List
    template_name = 'customer/customers.html'  # Template Name
    context_object_name = 'customers'  # Change default name of objectList
    ordering = ['-updated_at']  # Ordering post LIFO
    paginate_by = 20  # number of page I want to show in single page

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Customer List"
        context["nav_bar"] = "customer_list"
        context['customers'] = Customers.objects.all().order_by('-updated_at')
        print(context)
        return context


# def add_new_customers(request):
#     context = {'title': 'Add New Customer',
#                'nav_bar': 'add_new_customer',
#                }
#     return render(request, 'customer/add_new_customer.html', context)

def add_new_customers(request):
    print("called")
    template_name = 'customer/add_new_customer.html'

    if request.method == 'GET':
        print("called GET")
        customer_form = CustomerCreateForm(request.GET or None)

    elif request.method == 'POST':
        print("called POST")
        print(request.POST)
        customer_form = CustomerCreateForm(request.POST)

        if customer_form.is_valid():
            obj = customer_form.save(commit=False)
            obj.author = request.user
            obj.is_active = True
            obj.save()
            messages.add_message(request, messages.SUCCESS, 'New Customer Added Successfully!')
            return redirect('all-customers')

        else:
            print("Not Valid Create Form")
            print(customer_form.errors)

    return render(request, template_name, {
        'customer_form': customer_form,
        'title': 'Add New Customer',
        'nav_bar': 'add_new_customer',
    })
