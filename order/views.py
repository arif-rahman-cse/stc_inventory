from django.shortcuts import render


# Create your views here.

def orders(request):
    context = {'title': 'Orders List',
               'nav_bar': 'orders',
               }
    return render(request, 'order/orders.html', context)


def new_order(request):
    context = {'title': 'New Order',
               'nav_bar': 'new_order',
               }
    return render(request, 'order/new_order.html', context)
