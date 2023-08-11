from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from sales.models import Product
from .models import Cart, CartItem, SiteConfiguration
from django.http import JsonResponse
from .forms import SiteConfigurationForm
from django.http import HttpResponseBadRequest

# Create your views here.


def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def cart(request):
    total = 0
    quantity = 0
    cart_items = []

    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)

        total_tax = 0  # Initialize total_tax here

        for cart_item in cart_items:
            total += (cart_item.product.sale_price * cart_item.quantity)
            quantity += cart_item.quantity

            # Add tax amount of the current cart item to total_tax
            total_tax += cart_item.tax

    except ObjectDoesNotExist:
        pass

    site_config = SiteConfiguration.objects.first()
    shipping_cost = 0
    if site_config and total < site_config.shipping_threshold:
        shipping_cost = site_config.shipping_cost

    total_with_shipping = total + total_tax + shipping_cost

    context = {
        'cart_items': cart_items,
        'quantity': quantity,
        'total': total_with_shipping,
        'total_tax': total_tax,
        'shipping_cost': shipping_cost,
    }

    return render(request, 'sales/cart.html', context)


def add_cart(request, pk):
    product = Product.objects.get(id=pk)
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id=_cart_id(request))
    cart.save()

    tax_rate = product.tax_rate
    tax_amount = (product.sale_price * tax_rate / 100)

    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)
        cart_item.quantity += 1
        cart_item.tax = tax_amount * cart_item.quantity  # Recalculate tax amount
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            product=product,
            quantity=1,
            cart=cart,
            tax=tax_amount,  # Assign initial tax amount
        )
        cart_item.save()
    return redirect('cart')


def remove_cart(request, pk):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=pk)
    cart_item = CartItem.objects.get(product=product, cart=cart)

    # Calculate the tax amount for one item
    tax_rate = product.tax_rate
    tax_amount_per_item = (product.sale_price * tax_rate / 100)

    if cart_item.quantity > 1:
        # Decrease quantity and adjust tax amount
        cart_item.quantity -= 1
        cart_item.tax -= tax_amount_per_item
        cart_item.save()
    else:
        # Remove the cart item
        cart_item.delete()
    return redirect('cart')


def delete_cart_item(request, pk):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=pk)
    cart_item = CartItem.objects.get(cart=cart, product=product)
    cart_item.delete()
    return redirect('cart')
