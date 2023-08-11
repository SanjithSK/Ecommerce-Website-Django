from django.contrib import admin


from .models import Product, Category,  Sub_Category, brand, Review, tag


# Register your models here.


admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Sub_Category)
admin.site.register(Review)

admin.site.register(tag)
admin.site.register(brand)


class ProductAdmin(admin.ModelAdmin):
    pass
