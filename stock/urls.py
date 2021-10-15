from django.urls import path

from . import views

urlpatterns = [
    path('stock-ledger', views.StockLedgerListView.as_view(), name="stock-ledger"),
    path('new-lc', views.add_new_lc, name="new-lc"),
    path('add-stock', views.add_stock, name="add-stock"),
]
