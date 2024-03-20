from django.contrib import messages
from django.core.mail import EmailMessage
from django.http import FileResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CustomerForm, OrderForm, UpdateOrderForm
from .models import Customer, Invoice, Order
from .pdf import PDF

# This file contains the views for the sales module of the webcrm application.


# The home_sales view retrieves all customers and orders, ordered by the date they were created.
def home_sales(request):
    customers = Customer.objects.all().order_by("-date_created")
    orders = Order.objects.all().order_by("-date_created")
    return render(
        request, "sales/home_sales.html", {"customers": customers, "orders": orders}
    )


# The create_customer_view handles the creation of a new customer.
def create_customer_view(request):
    form = CustomerForm(request.POST or None)
    if form.is_valid():
        form.save()
        form = CustomerForm()
        return render(request, "sales/create_customer.html", {"form": form})
    if "cancel" in request.POST:
        return render(request, "sales/home_sales.html")
    return render(request, "sales/create_customer.html", {"form": form})


# The customer_delete_view handles the deletion of a customer.
def customer_delete_view(request, handle):
    customer = get_object_or_404(Customer, handle=handle)
    if request.method == "POST":
        customer.delete()
        return redirect("home_sales")
    return render(request, "sales/home_sales.html")


# The create_sales_order_view handles the creation of a new sales order.
def create_sales_order_view(request):
    form = OrderForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("home_sales")
    if "cancel" in request.POST:
        return render(request, "sales/home_sales.html")
    return render(request, "sales/create_order.html", {"form": form})


# The customer_detail_view handles the display and update of a customer's details.
def customer_detail_view(request, handle):
    customer = get_object_or_404(Customer, handle=handle)
    if request.method == "POST":
        if "delete" in request.POST:
            print("DELETE => ", request.POST)
            customer.delete()
            messages.success(request, "Customer deleted successfully")
            return redirect("home_sales")
        else:
            form = CustomerForm(request.POST, instance=customer)
            if form.is_valid():
                form.save()
                messages.success(request, "Customer updated successfully")
                return redirect("home_sales")
    else:
        form = CustomerForm(instance=customer)
    return render(
        request, "sales/customer_detail.html", {"form": form, "customer": customer}
    )


# The order_detail_view handles the display and update of an order's details.
def order_detail_view(request, order_id):
    order = get_object_or_404(Order, order_id=order_id)
    if request.method == "POST":
        if "delete" in request.POST:
            print("DELETE => ", request.POST)
            order.delete()
            messages.success(request, "Order deleted successfully")
            return redirect("home_sales")
        else:
            form = UpdateOrderForm(request.POST, instance=order)
            if form.is_valid():
                form.save()
                messages.success(request, "Order updated successfully")
                return redirect("home_sales")
    else:
        form = UpdateOrderForm(instance=order)
    return render(request, "sales/order_detail.html", {"form": form, "order": order})


# The send_email view handles the sending of an order confirmation email.
def send_email(request, order_id):
    order = get_object_or_404(Order, order_id=order_id)
    if request.method == "POST":
        subject = "Order Confirmation"
        message = (
            f"Hi {order.customer.name},\n\nYour order has been confirmed.\n\nOrder ID: "
            f"{order.order_id}\n\nProduct: {order.product.name}\n\nPrice: {order.product.price}\n\nQuantity: "
            f"{order.quantity}\n\nTotal: {order.total}\n\nThank you for shopping with us.\n\n"
            f"Best Regards,\n\nSales Team"
        )
        to_email = order.customer.email
        email = EmailMessage(subject, message, to=[to_email])
        email.send()
        return redirect("home_sales")
    return render(request, "sales/order_detail.html")


# The invoice_pdf_view handles the creation and download of an invoice in PDF format.
def invoice_pdf_view(request, order_id):
    order = get_object_or_404(Order, order_id=order_id)
    if request.method == "POST":
        invoice, created = Invoice.objects.get_or_create(order=order)
        pdf = PDF(f"{order.order_id}")
        pdf.create_invoice(invoice)

        f = open(pdf.file_name, "rb")
        response = FileResponse(f, content_type="application/pdf")
        response["Content-Disposition"] = f"attachment; filename={pdf.file_name}"
        return response
    return render(request, "sales/order_detail.html")
