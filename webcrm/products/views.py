from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ProductForm, ProductUpdateForm
from .models import Product


def create(request):
    """
    Handle the creation of a new product.

    This view handles the POST request for creating a new product. If the form is valid, it saves the product and redirects to the product creation page with a success message. If the user is not authenticated, it adds an error to the form.

    Args:
        request (HttpRequest): The request instance.

    Returns:
        HttpResponse: The response instance.
    """
    form = ProductForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        obj = form.save(commit=False)
        if request.user.is_authenticated:
            obj.save()
            messages.success(request, "Product created successfully")
            form = ProductForm()
            return render(request, "products/create.html", {"form": form})
        form.add_error(None, "You must be logged in to create a product")
    return render(request, "products/create.html", {"form": form})


def list_product_view(request):
    """
    Display a list of all products.

    This view handles the GET request for the product list page. It retrieves all products and orders them by timestamp in descending order.

    Args:
        request (HttpRequest): The request instance.

    Returns:
        HttpResponse: The response instance.
    """
    products = Product.objects.all().order_by("-timestamp")
    return render(request, "products/home_product.html", {"products": products})


def product_detail_view(request, handle):
    """
    Display the detail of a specific product and handle product updates and deletions.

    This view handles the GET and POST requests for the product detail page. If the request method is POST, it checks if the 'delete' or 'update' button was clicked and performs the corresponding action. If the request method is GET, it displays the product detail.

    Args:
        request (HttpRequest): The request instance.
        handle (str): The handle of the product.

    Returns:
        HttpResponse: The response instance.
    """
    product = get_object_or_404(Product, handle=handle)
    if request.method == "POST":
        if "delete" in request.POST:
            product.delete()
            messages.success(request, "Product deleted successfully")
            return redirect("home_product")
        elif "update" in request.POST:
            form = ProductForm(request.POST, request.FILES, instance=product)
            if form.is_valid():
                form.save()
                messages.success(request, "Product updated successfully")
                return redirect("home_product")
    else:
        form = ProductUpdateForm(instance=product)
    return render(
        request, "products/product_detail.html", {"form": form, "product": product}
    )
