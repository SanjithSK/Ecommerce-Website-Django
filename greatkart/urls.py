from django.urls import path
from . import views

urlpatterns = [
    path('cart/', views.cart, name="cart"),
    path('add-cart/<int:pk>/', views.add_cart, name="add-cart"),
    path('remove-cart/<int:pk>/', views.remove_cart, name="remove-cart"),
    path('delete-cart-item/<int:pk>/',
         views.delete_cart_item, name="delete-cart-item"),


]
