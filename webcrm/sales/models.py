from django.db import models

from products.models import Product
from products.tools.utils import random_slug_generator


# Create your models here.
class Customer(models.Model):
    name = models.CharField(max_length=200)
    first_name = models.CharField(max_length=200, null=True, blank=True)
    company = models.CharField(max_length=200, default='company name')
    handle = models.SlugField(max_length=230)
    phone = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    address = models.TextField(max_length=200)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.handle:
            self.handle = f"{self.name}-{random_slug_generator()}"
        super(Customer, self).save(*args, **kwargs)


class Order(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('SHIPPED', 'Shipped'),
        ('DELIVERED', 'Delivered'),
        # Add more status choices as needed
    ]
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2, editable=False, default=0.00)
    quantity = models.IntegerField(default=1)
    order_id = models.SlugField(max_length=230)
    date_created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        default='PENDING',
    )
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return self.order_id

    def save(self, *args, **kwargs):
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
        return self.product.price * self.quantity
