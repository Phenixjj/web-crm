from django import forms

from .models import Product


class ProductForm(forms.ModelForm):
    """
    A Django ModelForm for the Product model.

    This form is used to create and update instances of the Product model. It includes fields for the product's name, handle, price, description, and image.

    The form uses custom widgets for each field, and sets the label and placeholder attributes for each field in the form's constructor.

    Attributes:
        model: The model class that this form is associated with.
        fields: A list of the names of the model fields that should be included in the form.
        widgets: A dictionary mapping model field names to form widget classes.
    """

    class Meta:
        model = Product
        fields = ["name", "handle", "price", "description", "image"]

    widgets = {
        "name": forms.TextInput(attrs={"class": "form-control"}),
        "handle": forms.TextInput(attrs={"class": "form-control"}),
        "price": forms.NumberInput(attrs={"class": "form-control"}),
        "description": forms.Textarea(attrs={"class": "form-control"}),
        "image": forms.ImageField(),
    }

    def __init__(self, *args, **kwargs):
        """
        Initialize the form.

        This method sets the label and placeholder attributes for each field in the form.
        """
        super(ProductForm, self).__init__(*args, **kwargs)
        self.fields["name"].label = ""
        self.fields["handle"].label = ""
        self.fields["price"].label = ""
        self.fields["description"].label = ""
        self.fields["image"].label = "Image"

        self.fields["name"].widget.attrs["placeholder"] = "Product Name"
        self.fields["handle"].widget.attrs["placeholder"] = "Handle"
        self.fields["price"].widget.attrs["placeholder"] = "Price"
        self.fields["description"].widget.attrs["placeholder"] = "Description"
        self.fields["image"].widget.attrs["placeholder"] = "Image"


class ProductUpdateForm(ProductForm):
    """
    A Django ModelForm for updating instances of the Product model.

    This form inherits from ProductForm and disables the 'handle' field to prevent it from being changed during updates.
    """

    def __init__(self, *args, **kwargs):
        """
        Initialize the form.

        This method calls the parent form's constructor and then disables the 'handle' field.
        """
        super(ProductUpdateForm, self).__init__(*args, **kwargs)
        self.fields["handle"].disabled = True
