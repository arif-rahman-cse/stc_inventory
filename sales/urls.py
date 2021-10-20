from django.urls import path

from . import views

urlpatterns = [
    path('sales', views.sales, name="sales-list"),
    path('new-sales', views.new_sales, name="new-sales"),
    path('customer-information', views.customer_info, name="customer-information"),
]
