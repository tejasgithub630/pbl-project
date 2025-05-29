from django.contrib import admin
from .models import Product, Stock, Sale, Purchase

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name',  'price', 'current_stock', 'min_stock_level')
    list_filter = ('min_stock_level',)
    search_fields = ('name', 'description')

@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity', 'last_updated')
    list_filter = ('last_updated',)
    search_fields = ('product__name')

@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity', 'price_per_unit', 'total_price', 'date')
    list_filter = ('date',)
    search_fields = ('product__name', 'product__sku')
