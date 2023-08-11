from django import forms
from sales.models import Product, Category
from django.forms import inlineformset_factory


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'featured_image', 'gallery_image', 'short_description',
                  'description', 'tags', 'mrp', 'sale_price',
                  'category', 'sub_category', 'sku', 'total_stock']

    widgets = {
        'tags':  forms.CheckboxSelectMultiple(),
    }

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        field_names = ['name', 'featured_image', 'gallery_image', 'short_description',
                       'description',  'tags', 'mrp', 'sale_price',
                       'category', 'sub_category', 'sku', 'total_stock']

        for field_name in field_names:
            self.fields[field_name].widget.attrs.update(
                {'class': 'form-control'})
        self.fields['featured_image'].widget.attrs.update(
            {'class': 'file-upload-browse btn btn-primary'})
        self.fields['gallery_image'].widget.attrs.update(
            {'class': 'file-upload-browse btn btn-primary'})


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('image', 'name', 'is_active')

    def __init__(self, *args, **kwargs):
        super(CategoryForm, self).__init__(*args, **kwargs)
        field_names = ['image', 'name', 'is_active']
        for field_name in field_names:
            self.fields[field_name].widget.attrs.update(
                {'class': 'form-control'})
        self.fields['image'].widget.attrs.update(
            {'class': 'file-upload-browse btn btn-primary'})
