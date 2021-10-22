from django.urls import path

from . import views

urlpatterns = [
    path('sales', views.SalesListView.as_view(), name="sales-list"),
    path('new-sales', views.new_sales, name="new-sales"),
    path('sales-post/<str:invoice_no>', views.sales_post, name="transfer-stock-confirm"),
    # path('print_challan', views.print_challan, name='print-challan'),
    path('print_challan', views.GeneratePdf.as_view(), name='print-challan'),
    path('customer-information', views.customer_info, name="customer-information"),
    path('sales_item_popup', views.sales_item_popup, name='sales-item-popup'),
]
