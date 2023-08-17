from django.urls import path
from . import views

urlpatterns = [
    path('cart/', views.cart, name="cart"),
    path('add-cart/<int:pk>/', views.add_cart, name="add-cart"),
    path('remove-cart/<int:pk>/', views.remove_cart, name="remove-cart"),
    path('delete-cart-item/<int:pk>/',
         views.delete_cart_item, name="delete-cart-item"),
    path('wishlist/', views.wishlist, name="wishlist"),
    path('add-wishlist/<int:pk>/', views.add_to_wishlist, name="add-wishlist"),
    path('remove-wishlist/<int:pk>/', views.remove_wishlist_item, name="remove-wishlist"),
    path('add-wishlist-cart/<int:pk>/', views.add_wishlist_to_cart, name="add-wishlist-cart"),
    path('delete-wishlist-cart/<int:pk>/', views.delete_wishlist_item, name="delete-wishlist-cart"),         


]
