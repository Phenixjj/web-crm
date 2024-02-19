from django import forms
from .models import Product


class ProductForm(forms.ModelForm):
    """
    Form for the Product model
    """
    class Meta:
        model = Product
        fields = ['name', 'handle', 'price', 'description', 'image']

    widgets = {
        'name': forms.TextInput(attrs={'class': 'form-control'}),
        'handle': forms.TextInput(attrs={'class': 'form-control'}),
        'price': forms.NumberInput(attrs={'class': 'form-control'}),
        'description': forms.Textarea(attrs={'class': 'form-control'}),
        'image': forms.ImageField(),
    }

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = ''
        self.fields['handle'].label = ''
        self.fields['price'].label = ''
        self.fields['description'].label = ''
        self.fields['image'].label = 'Image'

        self.fields['name'].widget.attrs['placeholder'] = 'Product Name'
        self.fields['handle'].widget.attrs['placeholder'] = 'Handle'
        self.fields['price'].widget.attrs['placeholder'] = 'Price'
        self.fields['description'].widget.attrs['placeholder'] = 'Description'
        self.fields['image'].widget.attrs['placeholder'] = 'Image'


class ProductUpdateForm(ProductForm):
    def __init__(self, *args, **kwargs):
        super(ProductUpdateForm, self).__init__(*args, **kwargs)
        self.fields['handle'].disabled = True
