from django.contrib import admin
from .models import Product, ProductImage

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'is_featured')
    list_filter = ('is_featured',)
    search_fields = ('name',)
    inlines = [ProductImageInline]