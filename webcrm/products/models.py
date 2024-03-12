from django.core.files.storage import get_storage_class
from django.db import models

from .tools.utils import random_slug_generator, slugify_with_underscore


class Product(models.Model):
    """
    A Django Model for a Product.

    This model represents a product with fields for name, description, handle, price, image, image_url, timestamp, and updated.

    The handle field is automatically generated if not provided, and the image_url field is generated from the image field.

    Attributes:
        name (CharField): The name of the product.
        description (TextField): The description of the product.
        handle (SlugField): The unique handle of the product.
        price (DecimalField): The price of the product.
        image (ImageField): The image of the product.
        image_url (TextField): The URL of the product's image.
        timestamp (DateTimeField): The timestamp of when the product was created.
        updated (DateTimeField): The timestamp of when the product was last updated.
    """

    name = models.CharField(max_length=200)
    description = models.TextField(max_length=500)
    handle = models.SlugField(unique=True, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to="products/", blank=True, null=True)
    image_url = models.TextField(max_length=1024, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        """
        Return the string representation of the product.

        Returns:
            str: The name of the product.
        """
        return self.name

    def save(self, *args, **kwargs):
        """
        Save the product.

        This method overrides the default save method. If the handle field is not provided, it generates one. It also generates the image_url field from the image field.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        if not self.handle:
            handle = f"{self.name}-{random_slug_generator()}"
            self.handle = handle
        self.image_url = self.generate_s3_url("products")
        super().save(*args, **kwargs)

    def generate_s3_url(self, folder):
        """
        Generate the S3 URL for the product's image.

        This method generates the S3 URL for the product's image. If the image field is not provided, it returns a default URL.

        Args:
            folder (str): The folder where the image is stored.

        Returns:
            str: The S3 URL of the product's image.
        """
        try:
            if self.image:
                tmp = get_storage_class()().url(
                    f"{folder}/{slugify_with_underscore(self.image.name)}"
                )
                name = tmp.split("?")[0]
                return name.replace("minio", "localhost")
            else:
                return "http://127.0.0.1:9000/test/products/not-found.jpg"
        except Exception as e:
            print("ERROR => ", e)
