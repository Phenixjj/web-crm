from django.db import models
from tools.utils import random_slug_generator


# Create products model
class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(max_length=500)
    handle = models.SlugField(unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.handle == "":
            self.handle = f"{self.name}-{random_slug_generator}"
        super(Product, self).save(*args, **kwargs)


