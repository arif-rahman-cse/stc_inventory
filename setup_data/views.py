from django.shortcuts import render


# Create your views here.
def all_products(request):
    context = {'title': 'Product List',
               'nav_bar': 'product_list',
               }
    return render(request, 'product/products.html', context)


def add_new_product(request):
    context = {'title': 'Add New Product',
               'nav_bar': 'add_new_product',
               }
    return render(request, 'product/add_new_product.html', context)


def all_customers(request):
    context = {'title': 'Customer List',
               'nav_bar': 'customer_list',
               }
    return render(request, 'customer/customers.html', context)


def add_new_customers(request):
    context = {'title': 'Add New Customer',
               'nav_bar': 'add_new_customer',
               }
    return render(request, 'customer/add_new_customer.html', context)
