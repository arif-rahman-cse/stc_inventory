from django.contrib.auth.decorators import login_required
from django.shortcuts import render


# Create your views here.


# Create your views here.
@login_required
def stc_dashboard(request):
    context = {'title': 'Sales',
               'nav_bar': 'dashboard',
               }
    return render(request, 'main/dashboard.html', context)

