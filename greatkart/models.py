from django.db import models
from sales.models import Product
from django.contrib.auth.models import User

# Create your models here.


class Cart(models.Model):
    cart_id = models.CharField(max_length=250, blank=True)
    session_key = models.CharField(max_length=40, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.cart_id


class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)
    tax = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def sub_total(self):
        total_before_tax = self.product.sale_price * self.quantity
        total_with_tax = total_before_tax + self.tax
        return total_with_tax

    def __str__(self):
        return str(self.product)


class SiteConfiguration(models.Model):
    shipping_threshold = models.PositiveIntegerField(default=10000)
    shipping_cost = models.DecimalField(
        max_digits=10, decimal_places=2, default=100)







class Wishlist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user)
    






class WishlistItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    wishlist = models.ForeignKey(Wishlist, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)
    tax = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def sub_total(self):
        total_before_tax = self.product.sale_price * self.quantity
        total_with_tax = total_before_tax + self.tax
        return total_with_tax

    def __str__(self):
        return str(self.product)
