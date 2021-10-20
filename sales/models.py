from django.contrib.auth.models import User
from django.db import models
import datetime
from setup_data.models import Customers, Warehouse, Products


def invoice_no_generate():
    # GET Current Date
    today = datetime.date.today()

    # Format the date like (20-11-28 YY-MM-DD)
    today_string = today.strftime('%y%m')
    prefix = "STC" + today_string

    # For the very first time invoice_number is DD-MM-YY-0001
    next_invoice_no = '0001'

    # Get Last Employee Start With DNCC-MI-
    last_invoice_no = SalesParent.objects.filter(invoice_no__startswith=prefix).order_by('invoice_no').last()

    if last_invoice_no:
        # Cut 4 digit from the Right and converted to int (STC-YY-MM-:xxxx)
        last_invoice_four_digit = int(last_invoice_no.invoice_no[-4:])

        # Increment one with last five digit
        next_invoice_no = '{0:04d}'.format(last_invoice_four_digit + 1)

    # Return custom invoice number
    return prefix + next_invoice_no


class SalesParent(models.Model):
    created_at = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    updated_at = models.DateTimeField(blank=True, null=True, auto_now=True)
    order_date = models.DateField(blank=True, null=True)
    invoice_no = models.CharField(max_length=100, primary_key=True, default=invoice_no_generate)
    customer = models.ForeignKey(Customers, on_delete=models.DO_NOTHING, )
    address = models.CharField(max_length=200, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.DO_NOTHING, )
    total_amount = models.DecimalField(max_digits=20, decimal_places=2)
    paid_amount = models.DecimalField(max_digits=20, decimal_places=2, default=0.0)
    due_amount = models.DecimalField(max_digits=20, decimal_places=2, default=0.0)
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING, )
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.invoice_no


class SalesChild(models.Model):
    created_at = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    updated_at = models.DateTimeField(blank=True, null=True, auto_now=True)
    order_date = models.DateField(blank=True, null=True)
    product = models.ForeignKey(Products, on_delete=models.DO_NOTHING, )
    quantity = models.DecimalField(max_digits=20, decimal_places=2)
    price = models.DecimalField(max_digits=20, decimal_places=2)
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    invoice_no = models.ForeignKey(SalesParent, on_delete=models.DO_NOTHING, )
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING, )
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.invoice_no

    class Meta:
        unique_together = (('product', 'invoice_no'),)
