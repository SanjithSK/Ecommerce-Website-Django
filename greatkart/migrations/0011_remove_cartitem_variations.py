# Generated by Django 4.2.4 on 2023-08-11 10:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('greatkart', '0010_alter_cart_id_alter_cartitem_id_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartitem',
            name='variations',
        ),
    ]
