from django.contrib import messages
from django.shortcuts import render, redirect

from .forms import ProductForm
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
