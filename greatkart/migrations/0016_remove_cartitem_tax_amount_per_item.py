# Generated by Django 4.2.4 on 2023-08-11 13:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('greatkart', '0015_cartitem_tax_amount_per_item'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartitem',
            name='tax_amount_per_item',
        ),
    ]