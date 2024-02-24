import unidecode
from django.core.files.storage import get_storage_class
from django.db import models

from .tools.utils import random_slug_generator, slugify_with_underscore


# Create products model
class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(max_length=500)
    handle = models.SlugField(unique=True, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    image_url = models.TextField(max_length=1024, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.handle:
            handle = f"{self.name}-{random_slug_generator()}"
            self.handle = handle
        # super().save(*args, **kwargs)
        self.image_url = self.generate_s3_url('products')
        super().save(*args, **kwargs)

    def generate_s3_url(self, folder):
        try:
            if self.image:
                tmp = get_storage_class()().url(f"{folder}/{slugify_with_underscore(self.image.name)}")
                name = tmp.split("?")[0]
                # replace minio with localhost
                return name.replace("minio", "localhost")
            else:
                return "http://127.0.0.1:9000/test/products/not-found.jpg"
        except Exception as e:
            print("ERROR => ", e)
