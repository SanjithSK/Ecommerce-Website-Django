from django.shortcuts import render, redirect, get_object_or_404
from .models import Product
from greatkart.models import CartItem
from greatkart.views import _cart_id

# Create your views here.


def home(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'sales/index.html', context)


def product_details(request, pk):

    try:
        product = get_object_or_404(Product, id=pk)
        in_cart = CartItem.objects.filter(
            cart__cart_id=_cart_id(request), product=product).exists()

    except Exception as e:
        raise e

    is_out_of_stock = product.total_stock <= 0
    has_stock = product.total_stock > 0

    context = {'product': product, 'in_cart': in_cart,
               'is_out_of_stock': is_out_of_stock}
    return render(request, 'sales/product-details.html', context)
