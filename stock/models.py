from django.contrib.auth.models import User
from django.db import models
import datetime
from setup_data.models import Products, Warehouse


class LC(models.Model):
    created_at = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    updated_at = models.DateTimeField(blank=True, null=True, auto_now=True)
    date = models.DateField(blank=True, null=True)
    file_no = models.CharField(max_length=100, )
    status = models.CharField(max_length=20, default="Open")
    quantity = models.DecimalField(max_digits=20, decimal_places=2)
    product = models.ForeignKey(Products, on_delete=models.DO_NOTHING, )
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING, )
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.file_no

    class Meta:
        unique_together = (('file_no', 'date', 'product'),)


def transaction_no():
    # GET Current Date
    today = datetime.date.today()

    # Format the date like (20-11 YY-MM)
    today_string = today.strftime('%y%m')

    # For the very first time invoice_number is YY-MM-DD-001
    next_invoice_number = '000001'

    # Get Last Invoice Number of Current Year, Month and Day (20-11-28 YY-MM-DD)
    last_invoice = Stock.objects.filter(transaction_no__startswith=today_string).order_by('transaction_no').last()

    if last_invoice:
        # Cut 4 digit from the left and converted to int (2011:xxx)
        last_invoice_number = int(last_invoice.transaction_no[4:])

        # Increment one with last six digit
        next_invoice_number = '{0:06d}'.format(last_invoice_number + 1)

    # Return custom invoice number
    return today_string + next_invoice_number


class Stock(models.Model):
    transaction_no = models.CharField(max_length=100, primary_key=True, default=transaction_no)
    ref_number = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    updated_at = models.DateTimeField(blank=True, null=True, auto_now=True)
    stock_in_date = models.DateField(blank=True, null=True)
    product = models.ForeignKey(Products, on_delete=models.DO_NOTHING, )
    file_no = models.CharField(max_length=100, blank=True, null=True)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.DO_NOTHING, )
    quantity = models.DecimalField(max_digits=20, decimal_places=2)
    lc_per_dollar_cost_tk = models.DecimalField(max_digits=20, decimal_places=2)
    lc_unit_cost_usd = models.DecimalField(max_digits=20, decimal_places=2)
    lc_unit_cost_tk = models.DecimalField(max_digits=20, decimal_places=2)
    total_amount_tk = models.DecimalField(max_digits=20, decimal_places=2)
    type = models.CharField(max_length=100, blank=True, null=True)
    sign = models.IntegerField(blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING, )
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.file_no

