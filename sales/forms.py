from django import forms
from django.forms import modelformset_factory

from sales.models import SalesParent, SalesChild
from setup_data.models import Warehouse
from stock.models import LC, Stock, StockTransfer


class SalesCreateForm(forms.ModelForm):
    class Meta:
        model = SalesParent
        fields = (
            'customer', 'address', 'phone', 'warehouse', 'order_date',
            'total_amount', 'paid_amount', 'due_amount',)
        widgets = {
            'customer': forms.Select(
                attrs={'required': True, 'class': 'form-control', 'value': '', 'id': 'id_customer'}),
            'warehouse': forms.Select(attrs={'required': True, 'class': 'form-control', }),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'total_amount': forms.NumberInput(
                attrs={'class': 'form-control', 'value': '', 'id': 'id_total_amount'}),
            'paid_amount': forms.NumberInput(
                attrs={'class': 'form-control', 'value': '', 'id': 'id_paid_amount'}),
            'due_amount': forms.NumberInput(
                attrs={'class': 'form-control', 'readonly': 'readonly', 'value': '', 'id': 'id_due_amount'}),
            'order_date': forms.DateTimeInput(format='%Y-%m-%d %H:%M:%S',
                                              attrs={'required': True, 'class': 'form-control', 'type': 'date', }),
        }
        labels = {
            'customer': 'Customer Name',
            'address': 'Address',
            'phone': 'Phone',
            'warehouse': 'Warehouse Name',
            'order_date': 'Order Date',
            'total_amount': 'Total Amount',
            'paid_amount': 'Paid Amount',
            'due_amount': 'Due Amount',
        }


class SalesChildFormCreateForm(forms.ModelForm):
    class Meta:
        model = SalesChild
        fields = (
            'product', 'quantity', 'price', 'amount',)


SalesChildFormset = modelformset_factory(
    SalesChild,
    form=SalesChildFormCreateForm,
    extra=1,
    widgets={
        'product': forms.Select(attrs={'required': True, 'class': 'form-control', }),
        'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
        'price': forms.NumberInput(attrs={'class': 'form-control'}),
        'amount': forms.NumberInput(attrs={'class': 'form-control'}),
    },
)
