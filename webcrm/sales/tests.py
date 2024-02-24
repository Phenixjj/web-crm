import datetime as dt
import math

import pytest
from django.db import transaction
from django.test import TestCase, TransactionTestCase

from products.models import Product

from .forms import CustomerForm
from .models import Customer, Invoice, Order

# Create your tests here.


class CustomerTestCase(TransactionTestCase):
    @pytest.mark.django_db
    def test_create_customer(self):
        with transaction.atomic():
            Customer.objects.create(
                name="John",
                first_name="Doe",
                company="John's company",
                phone="1234567890",
                email="jlcg@outlook.fr",
                address="1234, rue de la rue"
            )
            customer = Customer.objects.get(name="John")
            assert customer.name == "John"
            assert customer.first_name == "Doe"
            assert customer.company == "John's company"
            assert customer.phone == "1234567890"
            assert customer.email == "jlcg@outlook.fr"
            assert customer.address == "1234, rue de la rue"

    @pytest.mark.django_db
    def test_update_customer(self):
        with transaction.atomic():
            customer, create = Customer.objects.get_or_create(
                name="John",
                first_name="Doe",
                company="John's company",
                phone="1234567890",
                email="jlcg@outlook.fr",
                address="1234, rue de la rue"
            )
            customer.name = "Jane"
            customer.save()
            customer = Customer.objects.get(name="Jane")
            assert customer.name == "Jane"
            assert customer.first_name == "Doe"
            assert customer.company == "John's company"
            assert customer.phone == "1234567890"
            assert customer.email == "jlcg@outlook.fr"
            assert customer.address == "1234, rue de la rue"

    @pytest.mark.django_db
    def test_delete_customer(self):
        with transaction.atomic():
            customer, create = Customer.objects.get_or_create(
                name="John",
                first_name="Doe",
                company="John's company",
                phone="1234567890",
                email="jlcg@outlook.fr",
                address="1234, rue de la rue"
            )
            customer.delete()
            with pytest.raises(Customer.DoesNotExist):
                Customer.objects.get(name="John")


class CustomerFormTest(TestCase):
    def test_form_validity(self):
        form_data = {
            'name': 'John',
            'first_name': 'Doe',
            'company': 'John\'s company',
            'phone': '1234567890',
            'email': 'jlcg@outlook.fr',
            'address': '1234, rue de la rue'
        }
        form = CustomerForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_invalidity(self):
        form_data = {
            'name': '',
            'first_name': 'Doe',
            'company': 'John\'s company',
            'phone': '1234567890',
            'email': 'jlcg@outlook.fr',
            'address': '1234, rue de la rue'
        }
        form = CustomerForm(data=form_data)
        self.assertFalse(form.is_valid())


class OrderTestCase(TransactionTestCase):
    def customer(self):
        customer = Customer.objects.create(
            name="John",
            first_name="Doe",
            company="John's company",
            phone="1234567890",
            email="jlcg@outlook.fr",
            address="1234, rue de la rue"
        )
        return customer

    def product(self):
        product = Product.objects.create(
            name="Cat Toy",
            description="coucou",
            price=3.14
        )
        return product

    @pytest.mark.django_db
    def test_create_order(self):
        customer = self.customer()
        product = self.product()
        with transaction.atomic():
            Order.objects.create(
                customer=customer,
                product=product,
                order_id="John-123456",
                price=3.14,
                quantity=2,
                status="PENDING",
                total=6.28
            )
            order = Order.objects.get(order_id="John-123456")
            assert order.customer == customer
            assert order.product.name == "Cat Toy"
            assert math.isclose(order.price, 3.14, rel_tol=1e-9, abs_tol=1e-9)
            assert order.quantity == 2
            assert order.status == "PENDING"
            assert math.isclose(order.total, 6.28, rel_tol=1e-9, abs_tol=1e-9)

    @pytest.mark.django_db
    def test_update_order(self):
        customer = self.customer()
        product = self.product()
        with transaction.atomic():
            order, create = Order.objects.get_or_create(
                customer=customer,
                product=product,
                order_id="John-123456",
                price=3.14,
                quantity=2,
                status="PENDING",
                total=6.28
            )
            order.status = "SHIPPED"
            order.save()
            order = Order.objects.get(order_id="John-123456")
            assert order.customer == customer
            assert order.product.name == "Cat Toy"
            assert math.isclose(order.price, 3.14, rel_tol=1e-9, abs_tol=1e-9)
            assert order.quantity == 2
            assert order.status == "SHIPPED"
            assert math.isclose(order.total, 6.28, rel_tol=1e-9, abs_tol=1e-9)


class InvoiceTestCase(TransactionTestCase):

    def customer(self):
        customer = Customer.objects.create(
            name="John",
            first_name="Doe",
            company="John's company",
            phone="1234567890",
            email="jlcg@outlook.fr",
            address="1234, rue de la rue"
        )
        return customer

    def product(self):
        product = Product.objects.create(
            name="Cat Toy",
            description="coucou",
            price=3.14
        )
        return product

    def order(self):
        customer = self.customer()
        product = self.product()
        order = Order.objects.create(
            customer=customer,
            product=product,
            order_id="John-123456",
            price=3.14,
            quantity=2,
            status="PENDING",
            total=6.28
        )
        return order

    def test_create_invoice(self):
        order = self.order()
        order_json = {
            "order_id": str(order.order_id),
            "customer": str(order.customer.name),
            "product": str(order.product.name),
            "price": str(order.price),
            "quantity": str(order.quantity),
            "status": order.status,
            "total": str(order.total),
            "date_created": str(order.date_created)
        }
        with transaction.atomic():
            Invoice.objects.create(
                order=order,
                invoice_order_id="INV-123456",
            )
            invoice = Invoice.objects.get(invoice_order_id="INV-123456")
            assert invoice.order.order_id == order.order_id
            assert math.isclose(invoice.total, order.total, rel_tol=1e-9, abs_tol=1e-9)
