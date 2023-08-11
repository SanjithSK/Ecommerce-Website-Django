from django.urls import path
from . import views

urlpatterns = [
    path('djadmin/', views.dashboard, name="admin-dashboard"),
    path('admin-products/', views.productList, name="admin-productList"),
    path('edit-products/<int:pk>/', views.edit_product, name="edit_product"),
    path('delete-objects/<int:pk>/', views.delete_object, name="delete_object"),
    path('create-product/', views.create_product, name="create-product"),
    path('admin-category/', views.categoryList, name="admin-category-list"),
    path('create-category/', views.create_category, name="create-category"),
    path('edit-category/<int:pk>/', views.edit_category, name="edit-category"),
    path('delete-category/<int:pk>/',
         views.deleteCategory, name="delete-category"),
    path('edit-site-configuration/', views.edit_site_configuration,
         name='edit-site-configuration'),


]
