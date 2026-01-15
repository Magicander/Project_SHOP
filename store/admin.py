from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Category, Brand, Product, Cart, CartItem, Review

admin.site.register(Category)
admin.site.register(Brand)

class ProductAdmin(admin.ModelAdmin):
    list_display = ["sku", "name", "price", "stock_count", "sale", "created_at"]
    list_filter = ["category", "brand", "sale", "created_at"]
    readonly_fields = ["created_at", "updated_at", "sku"]
    search_fields = ["name", "sku"]

admin.site.register(Product, ProductAdmin)

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'is_ordered', 'status', 'created_at']
    list_filter = ['status', 'is_ordered', 'created_at']
    list_editable = ['status']
    inlines = [CartItemInline]

class ActiveCartInline(admin.TabularInline):
    model = Cart
    fk_name = "user"
    verbose_name = "Koszyk"
    verbose_name_plural = "Koszyk"
    extra = 0
    show_change_link = True
    fields = ['created_at']
    readonly_fields = ['created_at']
    def get_queryset(self, request):
        return super().get_queryset(request).filter(is_ordered=False)
    
class HistoryCartInline(admin.TabularInline):
    model = Cart
    fk_name = "user"
    verbose_name = "Zrealizowane "
    verbose_name_plural = "Historia Zamówień"
    extra = 0
    show_change_link = True
    fields = ['ordered_at', 'is_ordered', 'status']
    readonly_fields = ['ordered_at', 'is_ordered']  
    def get_queryset(self, request):
        return super().get_queryset(request).filter(is_ordered=True)

class ReviewInline(admin.TabularInline):
    model = Review
    extra = 0
    readonly_fields = ('created_at',)
    fields = ('product', 'rating', 'content', 'created_at')
    can_delete = True

class UserAdmin(BaseUserAdmin):
    inlines = [ActiveCartInline, HistoryCartInline, ReviewInline]

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['product', 'user', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['content']
    readonly_fields = ['created_at']


admin.site.unregister(User)
admin.site.register(User, UserAdmin)

