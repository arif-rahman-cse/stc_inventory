from django.urls import path

from . import views

urlpatterns = [
    path('orders', views.orders, name="orders-list"),
    path('new_order', views.new_order, name="new-order"),
]
