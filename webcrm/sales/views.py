from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CustomerForm, OrderForm, UpdateOrderForm
from .models import Customer, Order


# Create your views here.
def home_sales(request):
    customers = Customer.objects.all().order_by('-date_created')
    orders = Order.objects.all().order_by('-date_created')
    return render(request, 'sales/home_sales.html', {'customers': customers, 'orders': orders})


def create_customer_view(request):
    form = CustomerForm(request.POST or None)
    if form.is_valid():
        form.save()
        form = CustomerForm()
        return render(request, 'sales/create_customer.html', {'form': form})
    if 'cancel' in request.POST:
        return render(request, 'sales/home_sales.html')
    return render(request, 'sales/create_customer.html', {'form': form})


def customer_delete_view(request, handle):
    customer = get_object_or_404(Customer, handle=handle)
    if request.method == 'POST':
        customer.delete()
        return redirect('home_sales')
    return render(request, 'sales/home_sales.html')


def create_sales_order_view(request):
    form = OrderForm(request.POST or None)
    if form.is_valid():
        form.save()
        form = OrderForm()
        return render(request, 'sales/create_order.html', {'form': form})
    if 'cancel' in request.POST:
        return render(request, 'sales/home_sales.html')
    return render(request, 'sales/create_order.html', {'form': form})


def customer_detail_view(request, handle):
    customer = get_object_or_404(Customer, handle=handle)
    if request.method == 'POST':
        if 'delete' in request.POST:
            print("DELETE => ", request.POST)
            customer.delete()
            messages.success(request, 'Customer deleted successfully')
            return redirect('home_sales')
        else:
            form = CustomerForm(request.POST, instance=customer)
            if form.is_valid():
                form.save()
                messages.success(request, 'Customer updated successfully')
                return redirect('home_sales')
    else:
        form = CustomerForm(instance=customer)
    return render(request, 'sales/customer_detail.html', {'form': form, 'customer': customer})


def order_detail_view(request, order_id):
    order = get_object_or_404(Order, order_id=order_id)
    if request.method == 'POST':
        if 'delete' in request.POST:
            print("DELETE => ", request.POST)
            order.delete()
            messages.success(request, 'Order deleted successfully')
            return redirect('home_sales')
        else:
            form = UpdateOrderForm(request.POST, instance=order)
            if form.is_valid():
                form.save()
                messages.success(request, 'Order updated successfully')
                return redirect('home_sales')
    else:
        form = UpdateOrderForm(instance=order)
    return render(request, 'sales/order_detail.html', {'form': form, 'order': order})
