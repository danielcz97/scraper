from django.contrib import admin
from django.utils.html import format_html
from .models import Product
from .filters import MultiSelectCategoryFilter
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from django.contrib.auth.models import User
from .models import Category, UserProfile

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'UserProfiles'
    fk_name = 'user'

class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(UserAdmin, self).get_inline_instances(request, obj)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Category)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user',)
    filter_horizontal = ('preferred_categories',)

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'category', 'website', 'shop', 'last_changes', 'colored_last_changes_details')
    search_fields = ('name', 'price', 'stock', 'category', 'website', 'shop')
    list_filter = ('shop', MultiSelectCategoryFilter, 'last_changes')
    ordering = ('-last_changes',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            user_profile = UserProfile.objects.get(user=request.user)
            preferred_categories = user_profile.preferred_categories.all()
            return qs.filter(category_fk__in=preferred_categories)
        return qs

    def colored_last_changes_details(self, obj):
        changes = obj.last_changes_details
        if changes is None:
            return ''
        
        if "Zmieniono cenę" in changes:
            return format_html('<span style="color: blue;">{}</span>', changes)
        elif "Zmieniono stock z 0" in changes:
            return format_html('<span style="color: green;">{}</span>', changes)
        elif "Zmieniono stock na 0" in changes:
            return format_html('<span style="color: red;">{}</span>', changes)
        return changes

    colored_last_changes_details.short_description = 'Last Changes Details'

admin.site.register(Product, ProductAdmin)
