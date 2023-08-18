from django.db import models
import uuid
from django.db.models.signals import pre_save
from django.dispatch import receiver
# Create your models here.


class Product(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)
    featured_image = models.ImageField(
        null=True, blank=True, default='default.jpg', upload_to='images')
    gallery_image = models.ImageField(
        null=True, blank=True, default='default.jpg', upload_to='images')
    created = models.DateTimeField(auto_now_add=True)
    short_description = models.TextField(null=True, max_length=400, blank=True)
    description = models.TextField(null=True, max_length=2000, blank=True)

    tags = models.ManyToManyField('tag', blank=True)
    mrp = models.IntegerField(default=0, null=True, blank=True)
    sale_price = models.IntegerField(default=0, null=True, blank=True)
    category = models.ForeignKey(
        'Category', on_delete=models.SET_NULL, null=True, blank=True)
    sub_category = models.ForeignKey(
        'Sub_Category', on_delete=models.SET_NULL, null=True, blank=True)
    brand = models.ForeignKey(
        'Brand', on_delete=models.SET_NULL, null=True, blank=True)
    sku = models.CharField(max_length=50, unique=True, blank=True)
    total_stock = models.PositiveIntegerField(default=0)
    # slug = models.SlugField(max_length=200, unique=True)
    is_available = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    tax_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    def __str__(self):
        return self.name


class Category(models.Model):
    STATUS_CHOICES = (
        (True, 'Active'),
        (False, 'Inactive'),
    )
    image = models.ImageField(
        null=True, blank=True, default='default.jpg', upload_to='images')
    name = models.CharField(max_length=200, blank=True, null=True)
    is_active = models.BooleanField(choices=STATUS_CHOICES, default=True)

    def __str__(self):
        return self.name


class Sub_Category(models.Model):
    STATUS_CHOICES = (
        (True, 'Active'),
        (False, 'Inactive'),
    )
    image = models.ImageField(
        null=True, blank=True, default='default.jpg', upload_to='images')
    name = models.CharField(max_length=200, blank=True, null=True)
    is_active = models.BooleanField(choices=STATUS_CHOICES, default=True)
    parent_category = models.ForeignKey(
        Category, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    visitor_name = models.CharField(max_length=255)
    rating = models.PositiveIntegerField(
        choices=((1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')))
    comment = models.TextField()

    class Meta:
        # Ensure one review per visitor per product
        unique_together = ('product', 'visitor_name')

    def __str__(self):
        return f"Review for {self.product} by {self.visitor_name}"


class brand(models.Model):
    STATUS_CHOICES = (
        (True, 'Active'),
        (False, 'Inactive'),
    )
    image = models.ImageField(
        null=True, blank=True, default='default.jpg', upload_to='images')
    name = models.CharField(max_length=200, blank=True, null=True)
    is_active = models.BooleanField(choices=STATUS_CHOICES, default=True)

    def __str__(self):
        return self.name


class tag(models.Model):
    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
