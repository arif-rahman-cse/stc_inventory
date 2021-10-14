from django.shortcuts import render


# Create your views here.


# Create your views here.
def stc_dashboard(request):
    context = {'title': 'Sales',
               'nav_bar': 'dashboard',
               }
    return render(request, 'main/dashboard.html', context)

