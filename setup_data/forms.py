from .models import Customers, Products, Category, Origin
from django import forms


class CustomerCreateForm(forms.ModelForm):
    class Meta:
        model = Customers
        fields = (
            'customer_code', 'customer_name', 'customer_address', 'phone', 'email', 'bin_no',)
        # reference link below
        # https://simpleisbetterthancomplex.com/tutorial/2018/11/28/advanced-form-rendering-with-django-crispy-forms.html#custom-fields-placement-with-crispy-forms
        widgets = {
            'customer_code': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'customer_name': forms.TextInput(attrs={'class': 'form-control'}),
            'customer_address': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'bin_no': forms.TextInput(attrs={'class': 'form-control'}),

        }


class ProductsCreateForm(forms.ModelForm):
    class Meta:
        model = Products
        fields = (
            'product_name', 'packing', 'price', 'category', 'origin',)
        # reference link below
        # https://simpleisbetterthancomplex.com/tutorial/2018/11/28/advanced-form-rendering-with-django-crispy-forms.html#custom-fields-placement-with-crispy-forms
        widgets = {
            'product_name': forms.TextInput(attrs={'class': 'form-control', }),
            'category': forms.Select(attrs={'required': True, 'class': 'form-control', }),
            'origin': forms.Select(attrs={'required': True, 'class': 'form-control', }),
            'packing': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),

        }
