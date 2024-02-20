from django import forms
from django_select2.forms import Select2Widget

from products.models import Product

from .models import Customer, Order


class CustomerForm(forms.ModelForm):
    """
    Form for the Customer model
    """
    class Meta:
        model = Customer
        fields = ['name', 'first_name', 'phone', 'email', 'company', 'address']

    widgets = {
        'name': forms.TextInput(attrs={'class': 'form-control'}),
        'first_name': forms.TextInput(attrs={'class': 'form-control'}),
        'phone': forms.TextInput(attrs={'class': 'form-control'}),
        'email': forms.TextInput(attrs={'class': 'form-control'}),
        'company': forms.TextInput(attrs={'class': 'form-control'}),
        'address': forms.Textarea(attrs={'class': 'form-control'}),

    }

    def __init__(self, *args, **kwargs):
        super(CustomerForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = ''
        self.fields['first_name'].label = ''
        self.fields['phone'].label = ''
        self.fields['email'].label = ''
        self.fields['company'].label = ''
        self.fields['address'].label = ''

        self.fields['name'].widget.attrs['placeholder'] = 'Name'
        self.fields['first_name'].widget.attrs['placeholder'] = 'First Name'
        self.fields['phone'].widget.attrs['placeholder'] = 'Phone'
        self.fields['email'].widget.attrs['placeholder'] = 'Email'
        self.fields['company'].widget.attrs['placeholder'] = 'Company'
        self.fields['address'].widget.attrs['placeholder'] = 'Address'


class OrderForm(forms.ModelForm):
    """
    Form for the Order model
    """
    product = forms.ModelChoiceField(
        queryset=Product.objects.all(),
        empty_label="Select Product",
        widget=Select2Widget)
    customer = forms.ModelChoiceField(
        queryset=Customer.objects.all(),
        empty_label="Select Customer",
        widget=Select2Widget)

    class Meta:
        model = Order
        fields = ['customer', 'product', 'quantity']

    widgets = {
        'customer': forms.Select(attrs={'class': 'form-control'}),
        'product': forms.Select(attrs={'class': 'form-control'}),
        'quantity': forms.NumberInput(attrs={'class': 'form-control'}),

    }

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        self.fields['customer'].label = ''
        self.fields['product'].label = ''
        self.fields['quantity'].label = ''

        self.fields['customer'].widget.attrs['placeholder'] = 'Customer'
        self.fields['product'].widget.attrs['placeholder'] = 'Product'
        self.fields['quantity'].widget.attrs['placeholder'] = 'Quantity'


class UpdateOrderForm(forms.ModelForm):
    """
    Form for the Update Order model
    """
    class Meta:
        model = Order
        fields = ['customer', 'product', 'status', 'quantity', 'total']

    widgets = {
        'customer': forms.Select(attrs={'class': 'form-control'}),
        'product': forms.Select(attrs={'class': 'form-control'}),
        'status': forms.Select(attrs={'class': 'form-control'}),
        'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
        'total': forms.NumberInput(attrs={'class': 'form-control', 'readonly': True}),
    }

    def __init__(self, *args, **kwargs):
        super(UpdateOrderForm, self).__init__(*args, **kwargs)
        self.fields['customer'].label = ''
        self.fields['product'].label = ''
        self.fields['status'].label = ''
        self.fields['quantity'].label = ''
        self.fields['total'].label = ''

        self.fields['customer'].widget.attrs['placeholder'] = 'Customer'
        self.fields['product'].widget.attrs['placeholder'] = 'Product'
        self.fields['status'].widget.attrs['placeholder'] = 'Status'
        self.fields['quantity'].widget.attrs['placeholder'] = 'Quantity'
        self.fields['total'].widget.attrs['placeholder'] = 'Total'

        self.fields['total'].disabled = True