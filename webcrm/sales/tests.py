import math

import pytest
from django.db import transaction
from django.test import TestCase, TransactionTestCase
from products.models import Product

from .forms import CustomerForm
from .models import Customer, Invoice, Order

# This file contains test cases for the Customer, Order, and Invoice models in the sales module.


class CustomerTestCase(TransactionTestCase):
    """
    This class contains test cases for the Customer model.
    """

    @pytest.mark.django_db
    def test_create_customer(self):
        """
        Test case for creating a new customer.
        """
        with transaction.atomic():
            # Create a new customer
            Customer.objects.create(
                name="John",
                first_name="Doe",
                company="John's company",
                phone="1234567890",
                email="jlcg@outlook.fr",
                address="1234, rue de la rue",
            )
            # Retrieve the created customer and assert the values
            customer = Customer.objects.get(name="John")
            assert customer.name == "John"
            assert customer.first_name == "Doe"
            assert customer.company == "John's company"
            assert customer.phone == "1234567890"
            assert customer.email == "jlcg@outlook.fr"
            assert customer.address == "1234, rue de la rue"

    @pytest.mark.django_db
    def test_update_customer(self):
        """
        Test case for updating an existing customer.
        """
        with transaction.atomic():
            # Create or get a customer
            customer, create = Customer.objects.get_or_create(
                name="John",
                first_name="Doe",
                company="John's company",
                phone="1234567890",
                email="jlcg@outlook.fr",
                address="1234, rue de la rue",
            )
            # Update the customer's name
            customer.name = "Jane"
            customer.save()
            # Retrieve the updated customer and assert the values
            customer = Customer.objects.get(name="Jane")
            assert customer.name == "Jane"
            assert customer.first_name == "Doe"
            assert customer.company == "John's company"
            assert customer.phone == "1234567890"
            assert customer.email == "jlcg@outlook.fr"
            assert customer.address == "1234, rue de la rue"

    @pytest.mark.django_db
    def test_delete_customer(self):
        """
        Test case for deleting a customer.
        """
        with transaction.atomic():
            # Create or get a customer
            customer, create = Customer.objects.get_or_create(
                name="John",
                first_name="Doe",
                company="John's company",
                phone="1234567890",
                email="jlcg@outlook.fr",
                address="1234, rue de la rue",
            )
            # Delete the customer
            customer.delete()
            # Assert that the customer does not exist
            with pytest.raises(Customer.DoesNotExist):
                Customer.objects.get(name="John")


class CustomerFormTest(TestCase):
    """
    This class contains test cases for the CustomerForm.
    """

    def test_form_validity(self):
        """
        Test case for a valid form.
        """
        # Define valid form data
        form_data = {
            "name": "John",
            "first_name": "Doe",
            "company": "John's company",
            "phone": "1234567890",
            "email": "jlcg@outlook.fr",
            "address": "1234, rue de la rue",
        }
        # Create a form with the valid data and assert that it is valid
        form = CustomerForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_invalidity(self):
        """
        Test case for an invalid form.
        """
        # Define invalid form data
        form_data = {
            "name": "",
            "first_name": "Doe",
            "company": "John's company",
            "phone": "1234567890",
            "email": "jlcg@outlook.fr",
            "address": "1234, rue de la rue",
        }
        # Create a form with the invalid data and assert that it is not valid
        form = CustomerForm(data=form_data)
        self.assertFalse(form.is_valid())


class OrderTestCase(TransactionTestCase):
    """
    This class contains test cases for the Order model.
    """

    def customer(self):
        """
        Helper method to create a customer.
        """
        customer = Customer.objects.create(
            name="John",
            first_name="Doe",
            company="John's company",
            phone="1234567890",
            email="jlcg@outlook.fr",
            address="1234, rue de la rue",
        )
        return customer

    def product(self):
        """
        Helper method to create a product.
        """
        product = Product.objects.create(
            name="Cat Toy", description="coucou", price=3.14
        )
        return product

    @pytest.mark.django_db
    def test_create_order(self):
        """
        Test case for creating a new order.
        """
        customer = self.customer()
        product = self.product()
        with transaction.atomic():
            # Create a new order
            Order.objects.create(
                customer=customer,
                product=product,
                order_id="John-123456",
                price=3.14,
                quantity=2,
                status="PENDING",
                total=6.28,
            )
            # Retrieve the created order and assert the values
            order = Order.objects.get(order_id="John-123456")
            assert order.customer == customer
            assert order.product.name == "Cat Toy"
            assert math.isclose(order.price, 3.14, rel_tol=1e-9, abs_tol=1e-9)
            assert order.quantity == 2
            assert order.status == "PENDING"
            assert math.isclose(order.total, 6.28, rel_tol=1e-9, abs_tol=1e-9)

    @pytest.mark.django_db
    def test_update_order(self):
        """
        Test case for updating an existing order.
        """
        customer = self.customer()
        product = self.product()
        with transaction.atomic():
            # Create or get an order
            order, create = Order.objects.get_or_create(
                customer=customer,
                product=product,
                order_id="John-123456",
                price=3.14,
                quantity=2,
                status="PENDING",
                total=6.28,
            )
            # Update the order's status
            order.status = "SHIPPED"
            order.save()
            # Retrieve the updated order and assert the values
            order = Order.objects.get(order_id="John-123456")
            assert order.customer == customer
            assert order.product.name == "Cat Toy"
            assert math.isclose(order.price, 3.14, rel_tol=1e-9, abs_tol=1e-9)
            assert order.quantity == 2
            assert order.status == "SHIPPED"
            assert math.isclose(order.total, 6.28, rel_tol=1e-9, abs_tol=1e-9)


class InvoiceTestCase(TransactionTestCase):
    """
    This class contains test cases for the Invoice model.
    """

    def customer(self):
        """
        Helper method to create a customer.
        """
        customer = Customer.objects.create(
            name="John",
            first_name="Doe",
            company="John's company",
            phone="1234567890",
            email="jlcg@outlook.fr",
            address="1234, rue de la rue",
        )
        return customer

    def product(self):
        """
        Helper method to create a product.
        """
        product = Product.objects.create(
            name="Cat Toy", description="coucou", price=3.14
        )
        return product

    def order(self):
        """
        Helper method to create an order.
        """
        customer = self.customer()
        product = self.product()
        order = Order.objects.create(
            customer=customer,
            product=product,
            order_id="John-123456",
            price=3.14,
            quantity=2,
            status="PENDING",
            total=6.28,
        )
        return order

    def test_create_invoice(self):
        """
        Test case for creating a new invoice.
        """
        order = self.order()
        order_json = {
            "order_id": str(order.order_id),
            "customer": str(order.customer.name),
            "product": str(order.product.name),
            "price": str(order.price),
            "quantity": str(order.quantity),
            "status": order.status,
            "total": str(order.total),
            "date_created": str(order.date_created),
        }
        with transaction.atomic():
            # Create a new invoice
            Invoice.objects.create(
                order=order,
                invoice_order_id="INV-123456",
            )
            # Retrieve the created invoice and assert the values
            invoice = Invoice.objects.get(invoice_order_id="INV-123456")
            assert invoice.order.order_id == order.order_id
            assert math.isclose(invoice.total, order.total, rel_tol=1e-9, abs_tol=1e-9)
