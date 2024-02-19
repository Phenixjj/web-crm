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


class SalesOrder(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order_id = models.SlugField(max_length=230)
    date_created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=200, default='Pending')
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.order_id

    def save(self, *args, **kwargs):
        if not self.order_id:
            self.order_id = f"{self.customer.name}-{random_slug_generator()}"
        super(SalesOrder, self).save(*args, **kwargs)
