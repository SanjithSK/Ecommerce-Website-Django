# Generated by Django 4.2.4 on 2023-08-18 06:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('greatkart', '0027_orderitem_order_products'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderitem',
            name='order',
        ),
        migrations.RemoveField(
            model_name='orderitem',
            name='product',
        ),
        migrations.DeleteModel(
            name='Order',
        ),
        migrations.DeleteModel(
            name='OrderItem',
        ),
    ]