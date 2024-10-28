from django import forms
from .models import ProductLot


class ProductLotForm(forms.ModelForm):
    class Meta:
        model = ProductLot
        fields = ['lot_number', 'internal_reference', 'product_name', 'quantity']
        widgets = {
            'lot_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter lot number'}),
            'internal_reference': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter internal reference'}),
            'product_name': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
        }
