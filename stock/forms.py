from django import forms

from stock.models import LC, Stock, StockTransfer


class LcCreateForm(forms.ModelForm):
    class Meta:
        model = LC
        fields = (
            'file_no', 'date', 'quantity', 'product',)
        widgets = {
            'file_no': forms.TextInput(attrs={'class': 'form-control', }),
            'product': forms.Select(attrs={'required': True, 'class': 'form-control', }),
            'quantity': forms.TextInput(attrs={'class': 'form-control'}),
            'date': forms.DateTimeInput(format='%Y-%m-%d %H:%M:%S',
                                        attrs={'required': True, 'class': 'form-control', 'type': 'date', }),
        }


class StockCreateForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = (
            'product', 'file_no', 'warehouse', 'quantity', 'stock_in_date',
            'lc_per_dollar_cost_tk', 'lc_unit_cost_usd', 'lc_unit_cost_tk', 'total_amount_tk',)
        widgets = {
            'product': forms.Select(attrs={'required': True, 'class': 'form-control', }),
            'file_no': forms.TextInput(attrs={'class': 'form-control', }),
            'warehouse': forms.Select(attrs={'required': True, 'class': 'form-control', }),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'value': '', 'id': 'id_quantity'}),
            'lc_per_dollar_cost_tk': forms.NumberInput(
                attrs={'class': 'form-control', 'value': '', 'id': 'id_lc_per_dollar_cost_tk'}),
            'lc_unit_cost_usd': forms.NumberInput(
                attrs={'class': 'form-control', 'value': '', 'id': 'id_lc_unit_cost_usd'}),
            'lc_unit_cost_tk': forms.NumberInput(
                attrs={'class': 'form-control', 'readonly': 'readonly', 'value': '', 'id': 'id_lc_unit_cost_tk'}),
            'total_amount_tk': forms.NumberInput(
                attrs={'class': 'form-control', 'readonly': 'readonly', 'value': '', 'id': 'id_total_amount_tk'}),
            'stock_in_date': forms.DateTimeInput(format='%Y-%m-%d %H:%M:%S',
                                                 attrs={'class': 'form-control', 'placeholder': 'Select a date',
                                                        'type': 'date'}),
        }
        labels = {
            'lc_per_dollar_cost_tk': 'LC-Tk. Cost(Type first)',
            'lc_unit_cost_usd': 'LC-USD Cost',
            'lc_unit_cost_tk': 'Total Cost',
            'total_amount_tk': 'Total Amount in Tk.',
        }


class StockTransferFrom(forms.ModelForm):
    class Meta:
        model = StockTransfer
        fields = (
            'stock_transfer_date', 'from_warehouse', 'to_warehouse', 'transfer_qty', 'product',)
        widgets = {
            'product': forms.Select(attrs={'required': True, 'class': 'form-control', 'value': '',
                                           'id': 'id_transferable_qty'}),
            'from_warehouse': forms.Select(
                attrs={'required': True, 'class': 'form-control', 'value': '', 'id': 'id_from_warehouse'}),
            'to_warehouse': forms.Select(attrs={'required': True, 'class': 'form-control', }),
            'transfer_qty': forms.NumberInput(attrs={'class': 'form-control'}),
            'stock_transfer_date': forms.DateTimeInput(format='%Y-%m-%d %H:%M:%S',
                                                       attrs={'required': True, 'class': 'form-control',
                                                              'type': 'date'}),
        }
