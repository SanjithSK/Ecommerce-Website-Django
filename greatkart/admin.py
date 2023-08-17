from django.contrib import admin
from .forms import SiteConfigurationForm
from .models import Cart, CartItem, SiteConfiguration,Wishlist, WishlistItem

# Define the SiteConfigurationAdmin with the custom form and list display


# Register your models here.
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Wishlist)
admin.site.register(WishlistItem)

# Register SiteConfiguration with the custom admin


class SiteConfigurationAdmin(admin.ModelAdmin):
    form = SiteConfigurationForm
    list_display = ['shipping_threshold', 'shipping_cost']


admin.site.register(SiteConfiguration, SiteConfigurationAdmin)
