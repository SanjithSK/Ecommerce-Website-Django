# Generated by Django 4.2.4 on 2023-08-11 13:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('greatkart', '0014_remove_cartitem_variation'),
        ('sales', '0016_variation_product_variations'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='variations',
        ),
        migrations.DeleteModel(
            name='Variation',
        ),
    ]
