from django.contrib import admin
from .models import Store, Product, Cart, CartItem, Order, OrderItem, Review, ResetToken


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ['name', 'owner', 'created_at', 'updated_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['name', 'description', 'owner__username']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'store', 'price', 'stock', 'created_at']
    list_filter = ['created_at', 'store']
    search_fields = ['name', 'description', 'store__name']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Product Information', {
            'fields': ('store', 'name', 'description', 'image')
        }),
        ('Pricing & Stock', {
            'fields': ('price', 'stock')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username']


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['cart', 'product', 'quantity']
    list_filter = ['cart']
    search_fields = ['product__name', 'cart__user__username']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'buyer', 'total_amount', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['buyer__username', 'id']
    readonly_fields = ['created_at']
    fieldsets = (
        ('Order Information', {
            'fields': ('buyer', 'total_amount', 'status')
        }),
        ('Timestamps', {
            'fields': ('created_at',)
        }),
    )


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product_name', 'quantity', 'price']
    list_filter = ['order']
    search_fields = ['product_name', 'order__buyer__username']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['product', 'buyer', 'rating', 'is_verified', 'created_at']
    list_filter = ['rating', 'is_verified', 'created_at']
    search_fields = ['product__name', 'buyer__username', 'comment']
    readonly_fields = ['created_at', 'is_verified']


@admin.register(ResetToken)
class ResetTokenAdmin(admin.ModelAdmin):
    list_display = ['user', 'used', 'expiry_date', 'created_at']
    list_filter = ['used', 'expiry_date', 'created_at']
    search_fields = ['user__username', 'token']
    readonly_fields = ['created_at']
