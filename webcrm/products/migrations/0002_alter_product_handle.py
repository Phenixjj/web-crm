# Generated by Django 5.0.2 on 2024-02-15 20:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='handle',
            field=models.SlugField(blank=True, null=True, unique=True),
        ),
    ]
