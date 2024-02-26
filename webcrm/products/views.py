from django.contrib import messages
# import get_object_or_404
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ProductForm, ProductUpdateForm
from .models import Product

# Create your views here.


def create(request):
    form = ProductForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        obj = form.save(commit=False)
        if request.user.is_authenticated:
            obj.save()
            messages.success(request, 'Product created successfully')
            form = ProductForm()
            return render(request, 'products/create.html', {'form': form})
        form.add_error(None, 'You must be logged in to create a product')
    return render(request, 'products/create.html', {'form': form})


def list_product_view(request):
    products = Product.objects.all().order_by('-timestamp')
    return render(request, 'products/home_product.html', {'products': products})


def product_detail_view(request, handle):
    product = get_object_or_404(Product, handle=handle)
    if request.method == 'POST':
        if 'delete' in request.POST:
            print("DELETE => ", request.POST)
            product.delete()
            messages.success(request, 'Product deleted successfully')
            return redirect('home_product')
        elif 'update' in request.POST:
            form = ProductForm(request.POST, request.FILES, instance=product)
            if form.is_valid():
                form.save()
                messages.success(request, 'Product updated successfully')
                return redirect('home_product')
    else:
        form = ProductUpdateForm(instance=product)
    return render(request, 'products/product_detail.html', {'form': form, 'product': product})
