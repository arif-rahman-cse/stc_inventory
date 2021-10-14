from django.urls import path

from . import views

urlpatterns = [
    path('', views.stc_dashboard, name="stc-dashboard"),
    # path('all-products', views.all_products, name="all-products"),
]