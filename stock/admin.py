from django.contrib import admin

# Register your models here.
from stock.models import LC, Stock, StockTransfer, StockPrime

admin.site.register(LC)
# admin.site.register(Stock)
admin.site.register(StockTransfer)


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ['transaction_no', 'stock_in_date', 'product', 'file_no', 'warehouse', 'quantity',
                    'lc_per_dollar_cost_tk', 'lc_unit_cost_usd', 'lc_unit_cost_tk', 'total_amount_tk',
                    'author', 'is_active']
    list_per_page = 50
    search_fields = ['transaction_no', ]


@admin.register(StockPrime)
class StockAdmin(admin.ModelAdmin):
    list_display = ['transaction_no', 'ref_number', 'stock_in_date', 'product', 'warehouse', 'quantity',
                    'total_amount_tk', 'type', 'sign', 'stock_transaction_type', 'author', 'is_active']
    list_per_page = 50
    search_fields = ['transaction_no', ]
