# Generated by Django 4.2.4 on 2023-08-17 08:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('greatkart', '0024_alter_wishlistitem_wishlist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wishlistitem',
            name='wishlist',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='greatkart.wishlist'),
        ),
    ]