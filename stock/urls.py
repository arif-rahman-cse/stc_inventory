from django.urls import path

from . import views

urlpatterns = [
    path('stock-in-list', views.StockInListView.as_view(), name="stock-in-list"),
    path('transfer-stock', views.transfer_stock, name="transfer-stock"),
    path('transfer-stock-confirm/<str:stock_transfer_no>', views.transfer_stock_confirm, name="transfer-stock-confirm"),
    path('transferable-stock-qty/', views.transferable_stock_qty, name="transferable-stock-qty"),
    path('new-lc', views.add_new_lc, name="new-lc"),
    path('add-stock', views.add_stock, name="add-stock"),
]
