from django.contrib import admin

from sales.models import SalesParent, SalesChild


@admin.register(SalesParent)
class StockAdmin(admin.ModelAdmin):
    list_display = ['order_date', 'invoice_no', 'customer', 'warehouse', 'total_amount', 'paid_amount',
                    'due_amount', ]
    list_per_page = 50
    search_fields = ['invoice_no', ]


@admin.register(SalesChild)
class StockAdmin(admin.ModelAdmin):
    list_display = ['order_date', 'invoice_no', 'product', 'quantity', 'price', 'amount', 'quantity',]
    list_per_page = 50
    search_fields = ['invoice_no', ]
