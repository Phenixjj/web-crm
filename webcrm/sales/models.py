import datetime as dt

from django.db import models
from django.utils import timezone
from products.models import Product
from products.tools.utils import random_slug_generator


# Create your models here.
class Customer(models.Model):
    """
    Customer model represents a customer in the system.
    It includes fields for name, first name, company, handle, phone, email, address, and date_created.
    The 'handle' field is automatically generated on save if not provided.
    """

    name = models.CharField(max_length=200)
    first_name = models.CharField(max_length=200, null=True, blank=True)
    company = models.CharField(max_length=200, default="company name")
    handle = models.SlugField(max_length=230)
    phone = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    address = models.TextField(max_length=200)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """
        Overrides the save method to automatically generate a handle if not provided.
        """
        if not self.handle:
            self.handle = f"{self.name}-{random_slug_generator()}"
        super(Customer, self).save(*args, **kwargs)


class Order(models.Model):
    """
    Order model represents an order in the system.
    It includes fields for customer, product, price, quantity, order_id, date_created, status, and total.
    The 'price', 'order_id', and 'total' fields are automatically calculated on save if not provided.
    """

    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("SHIPPED", "Shipped"),
        ("DELIVERED", "Delivered"),
        # Add more status choices as needed
    ]
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(
        max_digits=10, decimal_places=2, editable=False, default=0.00
    )
    quantity = models.IntegerField(default=1)
    order_id = models.SlugField(max_length=230)
    date_created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        default="PENDING",
    )
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return self.order_id

    def save(self, *args, **kwargs):
        """
        Overrides the save method to automatically calculate the price, order_id, and total if not provided.
        """
        if not self.price:
            self.price = self.product.price
        if not self.order_id:
            self.order_id = f"{self.customer.name}-{random_slug_generator()}"
        # Sum of the order total
        if self.total != self.product.price * self.quantity:
            self.total = self.get_total
        super(Order, self).save(*args, **kwargs)

    @property
    def get_total(self):
        """
        Calculates the total price of the order based on the product price and quantity.
        """
        return self.product.price * self.quantity


class Invoice(models.Model):
    """
    Invoice model represents an invoice in the system.
    It includes fields for order, date_created, due_date, status, total, invoice_order_id, and json.
    The 'total', 'due_date', 'invoice_order_id', and 'json' fields are automatically calculated on save if not provided.
    """

    id = models.AutoField(primary_key=True)
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField()
    status = models.CharField(max_length=50, default="PENDING")
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    invoice_order_id = models.SlugField(max_length=230)
    json = models.JSONField(null=True, blank=True)

    def __str__(self):
        return f"Invoice for {self.order.order_id}"

    def save(self, *args, **kwargs):
        """
        Overrides the save method to automatically calculate the total, due_date, invoice_order_id, and json if not provided.
        """
        if not self.total:
            self.total = self.order.total

        if not self.due_date:
            self.due_date = dt.datetime.now() + dt.timedelta(days=60)

        if not self.invoice_order_id:
            current_date = timezone.now()
            date_string = current_date.strftime("%Y-%m-%d")
            self.invoice_order_id = f"{date_string.replace('-', '')}-{str(self.id)}"

        if not self.json:
            self.json = self.to_json()
        super(Invoice, self).save(*args, **kwargs)

    def to_json(self):
        """
        Converts the invoice details to a JSON object.
        """
        return {
            "order_id": str(self.order.order_id),
            "product": str(self.order.product.name),
            "'quantity": str(self.order.quantity),
            "invoice_id": str(self.invoice_order_id),
            "total": str(self.total),
            "due_date": str(self.due_date),
            "status": str(self.order.status),
            "date_created": str(dt.datetime.now()),
        }
