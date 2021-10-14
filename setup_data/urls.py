from django.urls import path

from . import views

urlpatterns = [
    path('all-products', views.all_products, name="all-products"),
    path('add-new-product', views.add_new_product, name="add-new-product"),

    path('all-customers', views.all_customers, name="all-customers"),
    path('add-new-customer', views.add_new_customers, name="add-new-customer"),
]
