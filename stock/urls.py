from django.urls import path

from . import views

urlpatterns = [
    path('stock-in-list', views.StockInListView.as_view(), name="stock-in-list"),
    path('stocked-product-list', views.StockedProductListView.as_view(), name="stocked-product-list"),
    path('transfer-stock', views.transfer_stock, name="transfer-stock"),
    path('delete-transfer-stock/<str:stock_transfer_no>', views.delete_transfer_stock, name="delete-transfer-stock"),
    path('transfer-stock-confirm/<str:stock_transfer_no>', views.transfer_stock_confirm, name="transfer-stock-confirm"),
    path('transferable-stock-qty/', views.transferable_stock_qty, name="transferable-stock-qty"),
    path('new-lc', views.add_new_lc, name="new-lc"),
    path('new-lc-delete/<str:lc_transaction_no>', views.new_lc_delete, name="new-lc-delete"),
    path('new-lc-process/<str:lc_transaction_no>', views.new_lc_process, name="new-lc-process"),
    path('new-lc-closed/<str:lc_transaction_no>', views.new_lc_closed, name="new-lc-closed"),
    path('add-stock', views.add_stock, name="add-stock"),
    path('get-warehouse-name/', views.WarehouseList.as_view(), name='get-warehouse-name'),
]
