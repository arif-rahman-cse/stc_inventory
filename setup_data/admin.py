from django.contrib import admin
from .models import Customers, Products, Category, Origin, Warehouse

# Register your models here.
admin.site.register(Customers)
admin.site.register(Products)
admin.site.register(Category)
admin.site.register(Origin)
admin.site.register(Warehouse)
