from django.shortcuts import render, redirect, get_object_or_404
from sales.models import Product, Category
from .forms import ProductForm, CategoryForm
import uuid
from greatkart.models import SiteConfiguration
from greatkart.forms import SiteConfigurationForm

# Create your views here.


def dashboard(request):
    return render(request, 'customadmin/admin-dashboard.html')

# PRODUCT VIEWS


def productList(request):
    products = Product.objects.all()
    page = 'productList'
    for product in products:
        product.progress_width = (product.sale_price / 10000) * 100
    context = {'page': page, 'products': products}
    return render(request, 'customadmin/admin-list.html', context)


def edit_product(request, pk):
    page = 'product-edit'
    product = get_object_or_404(Product, id=pk)
    form = ProductForm(instance=product)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('admin-productList')
    else:
        form = ProductForm(instance=product)

    return render(request, 'customadmin/admin-forms.html', {'forms': form, 'product': product, 'page': page})


def delete_object(request, pk):
    object = get_object_or_404(Product, id=pk)

    if request.method == 'POST':
        object.delete()
        return redirect('admin-productList')

    return render(request, 'customadmin/delete-object.html', {'object': object})


def create_product(request):
    page = 'product-create'

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # Redirect to the product list after creation
            return redirect('admin-productList')
    else:
        form = ProductForm()

    return render(request, 'customadmin/admin-forms.html', {'forms': form, 'page': page})


def categoryList(request):
    categories = Category.objects.all()
    page = 'categoryList'
    context = {'page': page, 'categories': categories}
    return render(request, 'customadmin/admin-list.html', context)


def create_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            # Redirect to the category list view
            return redirect('admin-category-list')
    else:
        form = CategoryForm()

    page = 'createCategory'
    context = {'page': page, 'forms': form}
    return render(request, 'customadmin/admin-forms.html', context)


def edit_category(request, pk):
    category = get_object_or_404(Category, id=pk)
    form = CategoryForm(instance=category)
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES, instance=category)
        if form.is_valid():
            form.save()
            return redirect('admin-category-list')

    page = 'createCategory'
    context = {'page': page, 'forms': form}
    return render(request, 'customadmin/admin-forms.html', context)


def deleteCategory(request, pk):
    object = get_object_or_404(Category, id=pk)
    context = {'object': object}
    if request.method == 'POST':
        object.delete()
        return redirect('admin-category-list')
    return render(request, 'customadmin/delete-object.html', context)


def edit_site_configuration(request):
    # Assuming you only have one instance
    site_config = SiteConfiguration.objects.first()
    if request.method == 'POST':
        form = SiteConfigurationForm(request.POST, instance=site_config)
        if form.is_valid():
            form.save()
            return redirect('edit-site-configuration')
    else:
        form = SiteConfigurationForm(instance=site_config)

    context = {
        'form': form,
    }
    return render(request, 'customadmin/site_configuration_edit.html', context)
