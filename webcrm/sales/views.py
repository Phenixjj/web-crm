from django.shortcuts import render
from .forms import CustomerForm, SalesOrderForm

# Create your views here.
#
#
# def home_sales(request):
#     return render(request, 'home_sales.html')


def list_sales_views(request):
    return render(request, 'sales/home_sales.html', {})


def create_customer_view(request):
    form = CustomerForm(request.POST or None)
    if form.is_valid():
        form.save()
        form = CustomerForm()
        return render(request, 'sales/create_customer.html', {'form': form})
    if 'cancel' in request.POST:
        return render(request, 'sales/home_sales.html')
    return render(request, 'sales/create_customer.html', {'form': form})


def create_sales_order_view(request):
    form = SalesOrderForm(request.POST or None)
    if form.is_valid():
        form.save()
        form = SalesOrderForm()
        return render(request, 'sales/create_sale.html', {'form': form})
    if 'cancel' in request.POST:
        return render(request, 'sales/home_sales.html')
    return render(request, 'sales/create_sale.html', {'form': form})
