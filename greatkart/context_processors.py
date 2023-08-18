
from .models import CartItem, WishlistItem, Cart, Wishlist
from .views import _cart_id
from django.core.exceptions import ObjectDoesNotExist


def cart_counter(request):
    cart_count = 0
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_count = CartItem.objects.filter(
                cart=cart, is_active=True).count()
        except Cart.DoesNotExist:
            pass
    return {'cart_count': cart_count}


def wishlist_counter(request):
    wishlist_count = 0
    if request.user.is_authenticated:
        try:
            wishlist = Wishlist.objects.get(user=request.user)
            wishlist_count = WishlistItem.objects.filter(
                wishlist=wishlist, is_active=True).count()
        except Wishlist.DoesNotExist:
            pass
    return {'wishlist_count': wishlist_count}
