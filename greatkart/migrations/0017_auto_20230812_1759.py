# Generated by Django 3.0.5 on 2023-08-12 12:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('greatkart', '0016_remove_cartitem_tax_amount_per_item'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='cartitem',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='siteconfiguration',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
