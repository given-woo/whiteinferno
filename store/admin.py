from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)
admin.site.register(TextBanner)

class CollectionAdmin(admin.ModelAdmin):
    filter_horizontal = ('product',)

admin.site.register(Collection, CollectionAdmin)
admin.site.register(ImageBanner)
admin.site.register(TwoColumnSection)
