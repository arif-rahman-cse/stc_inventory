from django.urls import path

from . import views


urlpatterns = [
    path('all-products', views.AllProductsListView.as_view(), name="all-products"),
    path('add-new-product', views.add_new_product, name="add-new-product"),

    path('all-customers', views.AllCustomerListView.as_view(), name="all-customers"),
    path('add-new-customer', views.add_new_customers, name="add-new-customer"),
    # path('add-new-customer', views.NewCustomerCreateView.as_view(), name="add-new-customer"),
]
