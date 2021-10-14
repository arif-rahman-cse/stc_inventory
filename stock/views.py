from django.shortcuts import render


# Create your views here.

def stock(request):
    context = {'title': 'Stock List',
               'nav_bar': 'stock',
               }
    return render(request, 'product/products.html', context)
