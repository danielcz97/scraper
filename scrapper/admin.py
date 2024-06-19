from django.contrib import admin
from .models import Product
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'category', 'website', 'shop')
    search_fields = ('name', 'price', 'stock', 'category', 'website', 'shop')
    list_filter = ('shop', 'category' )
    ordering = ('name',)

admin.site.register(Product, ProductAdmin)