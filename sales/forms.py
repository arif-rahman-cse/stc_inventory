from django import forms
from django.forms import modelformset_factory

from sales.models import SalesParent, SalesChild
from setup_data.models import Products


class SalesCreateForm(forms.ModelForm):
    class Meta:
        model = SalesParent
        fields = (
            'customer', 'address', 'phone', 'warehouse', 'order_date', 'quantity',
            'total_amount', 'paid_amount', 'due_amount',)
        widgets = {
            'customer': forms.Select(
                attrs={'required': True, 'class': 'form-control', 'value': '', 'id': 'id_customer'}),
            'warehouse': forms.Select(attrs={'required': True, 'class': 'form-control', }),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'readonly': 'readonly', 'value': '', 'id': 'sales_total_qty'}),
            'total_amount': forms.NumberInput(attrs={'class': 'form-control', 'readonly': 'readonly', 'value': '', 'id': 'sales_total_amount'}),
            'paid_amount': forms.NumberInput(attrs={'class': 'form-control', 'value': '', 'id': 'sales_paid_amount'}),
            'due_amount': forms.NumberInput(attrs={'class': 'form-control', 'readonly': 'readonly', 'value': '', 'id': 'sales_due_amount'}),
            'order_date': forms.DateTimeInput(format='%Y-%m-%d %H:%M:%S', attrs={'required': True, 'class': 'form-control', 'type': 'date', }),
        }
        labels = {
            'customer': 'Customer Name',
            'address': 'Address',
            'phone': 'Phone',
            'warehouse': 'Warehouse Name',
            'order_date': 'Order Date',
            'quantity': 'Total Qty',
            'total_amount': 'Total Amount',
            'paid_amount': 'Paid Amount',
            'due_amount': 'Due Amount',
        }


class SalesChildFormCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product'].queryset = Products.objects.filter(is_active=True)
        self.fields['product'].widget.attrs.update(
            {'class': 'textinput form-control setprice product', 'min': '0', 'required': 'true'})

        self.fields['quantity'].widget.attrs.update(
            {'class': 'textinput form-control setprice quantity', 'min': '0', 'required': 'true'})
        self.fields['price'].widget.attrs.update(
            {'class': 'textinput form-control setprice price', 'min': '0', 'required': 'true'})
        self.fields['amount'].widget.attrs.update(
            {'class': 'textinput form-control setprice amount', 'min': '0', 'required': 'true', 'readonly': 'readonly',})

    class Meta:
        model = SalesChild
        fields = (
            'product', 'quantity', 'price', 'amount',)


SalesChildFormset = modelformset_factory(
    SalesChild,
    form=SalesChildFormCreateForm,
    extra=1,
    widgets={
        'product': forms.Select(attrs={'class': 'form-control'}),
        'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
        'price': forms.NumberInput(attrs={'class': 'form-control'}),
        'amount': forms.NumberInput(attrs={'class': 'form-control'}),
    },
)
