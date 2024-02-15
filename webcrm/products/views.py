from django.shortcuts import render

# Create your views here.


def home_product(request):
    return render(request, 'products/home_product.html', {})


def create(request):
    return render(request, 'products/create.html', {})