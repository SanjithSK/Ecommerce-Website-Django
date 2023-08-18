from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from sales.models import Product
from .models import Cart, CartItem, SiteConfiguration, Wishlist, WishlistItem
from django.http import JsonResponse
from .forms import SiteConfigurationForm
from django.http import HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


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
    total_tax = 0  # Initialize total_tax here

    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)

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
    base_total = total

    context = {
        'cart_items': cart_items,
        'quantity': quantity,
        'total': total_with_shipping,
        'total_tax': total_tax,
        'shipping_cost': shipping_cost,
        'base_total': base_total
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

    try:
        cart_item = CartItem.objects.get(cart=cart, product=product)
        cart_item.delete()

        # Reactivate the corresponding WishlistItem
        if request.user.is_authenticated and hasattr(request.user, 'wishlist'):
            try:
                wishlist_item = WishlistItem.objects.get(
                    product=product, wishlist=request.user.wishlist)
                wishlist_item.is_active = True
                wishlist_item.save()
            except WishlistItem.DoesNotExist:
                pass  # Handle the case where wishlist item doesn't exist

    except CartItem.DoesNotExist:
        pass  # Handle the case where cart item doesn't exist

    return redirect('cart')


@login_required(login_url='login')
def wishlist(request):
    total = 0
    quantity = 0
    wishlist_items = []
    total_tax = 0

    try:
        wishlist = Wishlist.objects.get(
            user=request.user)  # Use request.user directly
        wishlist_items = WishlistItem.objects.filter(
            wishlist=wishlist, is_active=True)

        for wishlist_item in wishlist_items:
            total += (wishlist_item.product.sale_price *
                      wishlist_item.quantity)
            total_tax += wishlist_item.tax
            quantity += wishlist_item.quantity
            print(len(wishlist_items))

    except Wishlist.DoesNotExist:
        wishlist = Wishlist.objects.create(user=request.user)

    context = {
        'wishlist_items': wishlist_items,
        'quantity': quantity,
        'total_tax': total_tax,
        'total': total,
    }

    return render(request, 'sales/wishlist.html', context)


@login_required(login_url='login')
def add_to_wishlist(request, pk):
    product = Product.objects.get(id=pk)
    try:
        wishlist = Wishlist.objects.get(user=request.user)

        # Check if the product is already in the wishlist
        try:
            wishlist_item = WishlistItem.objects.get(
                product=product, wishlist=wishlist)

            # Product already in the wishlist, update quantity and tax
            wishlist_item.quantity += 1
            tax_rate = product.tax_rate
            tax_amount = (product.sale_price * tax_rate / 100)
            wishlist_item.tax = tax_amount * wishlist_item.quantity
            wishlist_item.save()

        except WishlistItem.DoesNotExist:
            # Product not in the wishlist, create a new wishlist item
            tax_rate = product.tax_rate
            tax_amount = (product.sale_price * tax_rate / 100)
            wishlist_item = WishlistItem.objects.create(
                product=product,
                quantity=1,
                wishlist=wishlist,
                tax=tax_amount,
            )

    except Wishlist.DoesNotExist:
        # Wishlist doesn't exist for the user, create a new wishlist and wishlist item
        wishlist = Wishlist.objects.create(user=request.user)
        tax_rate = product.tax_rate
        tax_amount = (product.sale_price * tax_rate / 100)
        wishlist_item = WishlistItem.objects.create(
            product=product,
            quantity=1,
            wishlist=wishlist,
            tax=tax_amount,
        )

    return redirect('wishlist')


def remove_wishlist_item(request, pk):
    user = request.user  # Get the User instance

    try:
        wishlist = Wishlist.objects.get(user=user)
        product = get_object_or_404(Product, id=pk)
        wishlist_item = WishlistItem.objects.get(
            product=product, wishlist=wishlist)

        if wishlist_item.quantity > 1:
            # Decrease quantity
            wishlist_item.quantity -= 1
            wishlist_item.save()
        else:
            # Remove the wishlist item
            wishlist_item.delete()

    except (Wishlist.DoesNotExist, WishlistItem.DoesNotExist):
        pass  # Handle the case where wishlist or wishlist item doesn't exist

    return redirect('wishlist')


@login_required(login_url='login')
def add_wishlist_to_cart(request, pk):
    user = request.user

    try:
        wishlist = Wishlist.objects.get(user=user)
        # Retrieve the Product based on pk
        product = Product.objects.get(pk=pk)

        # Retrieve the WishlistItem based on the product and wishlist
        try:
            wishlist_item = WishlistItem.objects.get(
                product=product, wishlist=wishlist, is_active=True)
            print("Wishlist Item Product:", wishlist_item.product)

            cart, created = Cart.objects.get_or_create(
                cart_id=_cart_id(request))

            try:
                cart_item = CartItem.objects.get(
                    cart=cart, product=wishlist_item.product)

                # Update existing cart item
                cart_item.quantity += wishlist_item.quantity
                cart_item.tax += wishlist_item.tax
                cart_item.save()

            except CartItem.DoesNotExist:
                # Create new cart item
                cart_item = CartItem.objects.create(
                    cart=cart,
                    product=wishlist_item.product,
                    quantity=wishlist_item.quantity,
                    tax=wishlist_item.tax,
                )

            wishlist_item.is_active = True  # Deactivate wishlist item after adding to cart
            wishlist_item.save()

        except WishlistItem.DoesNotExist:
            pass  # Handle the case where wishlist item doesn't exist

    except Wishlist.DoesNotExist:
        pass  # Handle the case where wishlist doesn't exist

    return redirect('cart')


def delete_wishlist_item(request, pk):
    user = request.user
    wishlist = Wishlist.objects.get(user=user)
    product = get_object_or_404(Product, id=pk)
    try:
        wishlist_item = WishlistItem.objects.get(
            product=product, wishlist=wishlist, is_active=True)
        wishlist_item.delete()

    except WishlistItem.DoesNotExist:
        pass  # Handle the case where wishlist item doesn't exist

    return redirect('wishlist')
