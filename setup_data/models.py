from django.db import models
from django.contrib.auth.models import User


def customer_code():
    prifix = "STC-"
    next_number = '00001'
    last_number = Customers.objects.filter(customer_code__startswith=prifix).order_by('customer_code').last()
    if last_number:
        last_code = int(last_number.customer_code[4:])
        next_number = '{0:05d}'.format(last_code + 1)
    return prifix + next_number


class Customers(models.Model):
    created_at = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    updated_at = models.DateTimeField(blank=True, null=True, auto_now=True)
    customer_code = models.CharField(max_length=20, primary_key=True, default=customer_code)
    customer_name = models.CharField(max_length=100, )
    customer_address = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)
    bin_no = models.CharField(max_length=100, blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING, )
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.customer_name


class Origin(models.Model):
    created_at = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    updated_at = models.DateTimeField(blank=True, null=True, auto_now=True)
    origin_name = models.CharField(max_length=50)
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING, )
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.origin_name


class Category(models.Model):
    created_at = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    updated_at = models.DateTimeField(blank=True, null=True, auto_now=True)
    category_name = models.CharField(max_length=100)
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING, )
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.category_name


class Products(models.Model):
    created_at = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    updated_at = models.DateTimeField(blank=True, null=True, auto_now=True)
    product_name = models.CharField(max_length=100, )
    packing = models.CharField(max_length=20, blank=True, null=True)
    price = models.DecimalField(max_digits=20, decimal_places=2)
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING, )
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, )
    origin = models.ForeignKey(Origin, on_delete=models.DO_NOTHING, )
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.product_name


class Warehouse(models.Model):
    created_at = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    updated_at = models.DateTimeField(blank=True, null=True, auto_now=True)
    warehouse_name = models.CharField(max_length=100)
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING, )
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.warehouse_name
