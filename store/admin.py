from django.contrib import admin

from .models import Category, Brand, Product, Cart, CartItem

admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(Cart)
admin.site.register(CartItem)


class Admin(admin.ModelAdmin):
    list_display = ["sku", "name", "price", "stock_count", "sale", "created_at"]
    list_filter = ["category", "brand", "sale", "created_at"]
    readonly_fields = ["created_at", "updated_at", "sku"]

admin.site.register(Product, Admin)
