from django import forms
from .models import Product


class ProductForm(forms.ModelForm):
    """
    Form for the Product model
    """
    class Meta:
        model = Product
        fields = ['name', 'price', 'description']

    widgets = {
        'name': forms.TextInput(attrs={'class': 'form-control'}),
        'price': forms.NumberInput(attrs={'class': 'form-control'}),
        'description': forms.Textarea(attrs={'class': 'form-control'}),
    }

    def clean_price(self):
        """
        Ensure the price is not negative
        """
        price = self.cleaned_data.get('price')
        if price and price < 0:
            raise forms.ValidationError('Price cannot be negative.')
        return price
