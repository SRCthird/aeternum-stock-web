from django import forms
from .models import InventoryTransfer, InventoryBay, ProductLot


class ProductLotForm(forms.ModelForm):
    class Meta:
        model = ProductLot
        fields = ['lot_number', 'internal_reference',
                  'product_name', 'quantity']
        widgets = {
            'lot_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter lot number'}),
            'internal_reference': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter internal reference'}),
            'product_name': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
        }


class InventoryTransferForm(forms.ModelForm):
    class Meta:
        model = InventoryTransfer
        fields = ['product_lot', 'from_inventory_bay',
                  'to_inventory_bay', 'quantity']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['from_inventory_bay'].queryset = InventoryBay.objects.filter(
            active=True)
        self.fields['to_inventory_bay'].queryset = InventoryBay.objects.filter(
            active=True)
        self.fields['product_lot'].queryset = ProductLot.objects.all()
