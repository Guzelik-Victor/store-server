from django import forms
from .models import Product
from django.core.exceptions import ValidationError


class QuantityForm(forms.Form):
    product_id = forms.DecimalField(widget=forms.HiddenInput())
    quantity = forms.DecimalField(
        min_value=0,
        widget=forms.NumberInput()
        )

    def clean(self):
        cleaned_data = super().clean()
        product_id = cleaned_data.get('product_id')
        quantity = cleaned_data.get('quantity')
        product = Product.objects.get(id=product_id)
        if quantity > product.quantity:
            msg = f'Количество товара на складе {product.quantity}'
            self.add_error('quantity', msg)


