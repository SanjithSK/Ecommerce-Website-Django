# Generated by Django 4.2.4 on 2023-08-11 12:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0015_delete_variation'),
    ]

    operations = [
        migrations.CreateModel(
            name='Variation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='variations',
            field=models.ManyToManyField(blank=True, to='sales.variation'),
        ),
    ]