from django import forms
from .models import InventoryTransfer, InventoryBay, ProductLot, InventoryBayLot


class ProductLotForm(forms.ModelForm):
    comment = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Add a comment for history'
        }),
        label="History Comment"
    )

    class Meta:
        model = ProductLot
        fields = ['lot_number', 'internal_reference',
                  'product_name', 'quantity']
        widgets = {
            'lot_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter lot number'}),
            'internal_reference': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter internal reference'}),
            'product_name': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        }

    def save(self, commit=True):
        instance = super().save(commit=False)
        comment = self.cleaned_data.get("comment")
        if comment:
            pass
        if commit:
            instance.save()
        return instance


class InventoryTransferForm(forms.ModelForm):
    class Meta:
        model = InventoryTransfer
        fields = ['product_lot', 'from_inventory_bay',
                  'to_inventory_bay', 'quantity', 'comments']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['from_inventory_bay'].required = True
        self.fields['from_inventory_bay'].queryset = InventoryBay.objects.filter(
            active=True)
        self.fields['to_inventory_bay'].required = True
        self.fields['to_inventory_bay'].queryset = InventoryBay.objects.filter(
            active=True)
        self.fields['product_lot'].required = True
        self.fields['product_lot'].queryset = ProductLot.objects.all()


class InventoryBayLotForm(forms.ModelForm):
    change_reason = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'rows': 3}),
        label="Change Reason",
        help_text="Provide a reason for this change (optional)."
    )

    class Meta:
        model = InventoryBayLot
        fields = '__all__'
