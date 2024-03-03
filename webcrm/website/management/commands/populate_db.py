from decimal import Decimal
from random import randint

from faker import Faker
from faker_commerce import Provider
from django.core.management.base import BaseCommand

from products.models import Product
from products.tools.utils import random_integer_generator, random_slug_generator
from sales.models import Customer, Order, Invoice


class Command(BaseCommand):
    help = 'Populate the database with fake data'

    def handle(self, *args, **kwargs):
        fake = Faker()
        fake.add_provider(Provider)
        for _ in range(10):  # Adjust the range as needed
            # Create fake data for each field in your models
            customer = Customer.objects.create(
                name=fake.name(),
                first_name=fake.first_name(),
                company=fake.company(),
                handle=fake.slug(),
                phone=fake.phone_number(),
                email=fake.email(),
                address=fake.address(),
            )
            product = Product.objects.create(
                name=fake.ecommerce_name(),
                description=fake.ecommerce_category(),
                price=Decimal(format(fake.ecommerce_price()/2000, '.2f'))
            )
            product.save()
            #
            order = Order.objects.create(
                customer=customer,
                product=product,
                quantity=randint(1, 10),
            )
            order.save()

            # Invoice.objects.create(
            #     order=order,
            #     due_date=fake.date_time_between(start_date='+1d', end_date='+60d'),
            #     # Fill in the rest of the fields for the Invoice model
            # )
            customer.save()
        self.stdout.write(self.style.SUCCESS('customer populated successfully'))

