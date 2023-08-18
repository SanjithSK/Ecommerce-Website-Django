from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('product-details/<int:pk>/',
         views.product_details, name="product-details"),
    path('shop/', views.shop, name="shop"),
]
