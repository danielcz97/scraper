from django.contrib import admin
from .models import Product
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'category', 'website', 'shop', 'last_changes')
    search_fields = ('name', 'price', 'stock', 'category', 'website', 'shop')
    list_filter = ('shop', 'category', 'last_changes' )
    ordering = ('last_changes',)

admin.site.register(Product, ProductAdmin)