import math

import pytest
from django.db import transaction
from django.test import TestCase, TransactionTestCase

from .forms import ProductForm
from .models import Product


class ProductTestCase(TransactionTestCase):
    """
    A Django TransactionTestCase for the Product model.

    This test case includes tests for creating, updating, deleting, and checking the handle and image_url generation of a product.
    """

    @pytest.mark.django_db
    def test_create_product(self):
        """
        Test the creation of a product.

        This test creates a product and then retrieves it to check that the fields were correctly set.
        """
        with transaction.atomic():
            Product.objects.create(name="Cat Toy", description="coucou", price=3.14)
            product = Product.objects.get(name="Cat Toy")
            assert product.name == "Cat Toy"
            assert product.description == "coucou"
            assert math.isclose(product.price, 3.14, rel_tol=1e-9, abs_tol=1e-9)

    @pytest.mark.django_db
    def test_update_product(self):
        """
        Test the update of a product.

        This test creates a product, updates its name, and then retrieves it to check that the name was correctly updated.
        """
        with transaction.atomic():
            product, create = Product.objects.get_or_create(
                name="Cat Toy", description="coucou", price=3.14
            )
            product.name = "Dog Toy"
            product.save()
            product = Product.objects.get(name="Dog Toy")
            assert product.name == "Dog Toy"
            assert product.description == "coucou"
            assert math.isclose(product.price, 3.14, rel_tol=1e-9, abs_tol=1e-9)

    @pytest.mark.django_db
    def test_delete_product(self):
        """
        Test the deletion of a product.

        This test creates a product, deletes it, and then tries to retrieve it to check that it was correctly deleted.
        """
        with transaction.atomic():
            product, create = Product.objects.get_or_create(
                name="Cat Toy", description="coucou", price=3.14
            )
            product.delete()
            with pytest.raises(Product.DoesNotExist):
                Product.objects.get(name="Cat Toy")

    @pytest.mark.django_db
    def test_gen_handle(self):
        """
        Test the generation of a product's handle.

        This test creates a product and then checks that a handle was correctly generated.
        """
        with transaction.atomic():
            product = Product.objects.create(
                name="Cat Toy", description="coucou", price=3.14
            )
            assert product.handle is not None
            assert product.handle[:7] == "Cat Toy"

    @pytest.mark.django_db
    def test_gen_image_url(self):
        """
        Test the generation of a product's image_url.

        This test creates a product with an image and then checks that an image_url was correctly generated.
        """
        with transaction.atomic():
            product = Product.objects.create(
                name="Cat Toy", description="coucou", price=3.14, image="test.jpg"
            )
            assert product.image_url == "http://localhost:9000/test/products/test.jpg"


class ProductFormTest(TestCase):
    """
    A Django TestCase for the ProductForm.

    This test case includes tests for checking the validity and invalidity of a form.
    """

    def test_form_validity(self):
        """
        Test the validity of a form.

        This test creates a form with valid data and then checks that the form is valid.
        """
        form_data = {
            "name": "Test Product",
            "handle": "test-product",
            "price": 10.99,
            "description": "This is a test product",
            "image": None,  # You can also test with an actual image file
        }
        form = ProductForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_invalidity(self):
        """
        Test the invalidity of a form.

        This test creates a form with invalid data (missing name) and then checks that the form is invalid.
        """
        form_data = {
            "name": "",  # name is required, so the form should be invalid
            "handle": "test-product",
            "price": 10.99,
            "description": "This is a test product",
            "image": None,
        }
        form = ProductForm(data=form_data)
        self.assertFalse(form.is_valid())
