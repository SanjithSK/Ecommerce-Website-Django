from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Category, brand
from greatkart.models import CartItem
from greatkart.views import _cart_id
from decimal import Decimal
from django.db.models import Count


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


def shop(request):
    categories = Category.objects.all()
    brands = brand.objects.all()
    cheap_products = Product.objects.all()

    products = Product.objects.all()

    category = request.GET.get('category')
    if category:
        products = products.filter(category__name=category)

    min_price = Decimal(request.GET.get('min_price', 0))
    max_price = Decimal(request.GET.get('max_price', '100000'))

    products = products.filter(
        sale_price__gte=min_price, sale_price__lte=max_price)

    sort_by = request.GET.get('sort_by')
    if sort_by == 'price_low_high':
        products = products.order_by('sale_price')
    elif sort_by == 'price_high_low':
        products = products.order_by('-sale_price')
    elif sort_by == 'created':
        products = products.order_by('-created_date')

    in_stock = request.GET.get('in_stock')
    if in_stock:
        products = products.filter(total_stock__gt=0)

    sorting_options = [
        {'value': '', 'label': 'Default sorting'},
        {'value': 'price_low_high', 'label': 'Sort by price: low to high'},
        {'value': 'price_high_low', 'label': 'Sort by price: high to low'},
        {'value': 'created', 'label': 'Sort by Newest First'},
    ]

    context = {
        'products': products,
        'categories': categories,
        'brands': brands,
        'cheap_products': cheap_products,
        'sorting_options': sorting_options,
        'selected_sort': sort_by,
        'selected_category': category,
        'min_price': min_price,
        'max_price': max_price,
    }
    return render(request, 'sales/shop.html', context)
