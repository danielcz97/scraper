from django.contrib.admin import SimpleListFilter
from django.utils.translation import gettext_lazy as _
from .models import Product
from urllib.parse import quote
class MultiSelectCategoryFilter(SimpleListFilter):
    title = _('Category')
    parameter_name = 'category'

    template = 'admin/custom_filter.html'

    def lookups(self, request, model_admin):
        self.request = request  # Przechowaj request
        shop = request.GET.get('shop')
        print(shop)
        if shop:
            categories = Product.objects.filter(shop=shop).values_list('category', flat=True).distinct()
            print(categories)
        else:
            categories = Product.objects.values_list('category', flat=True).distinct()
        return [(category, category) for category in categories]

    def queryset(self, request, queryset):
        if self.value():
            selected_categories = self.value()
            return queryset.filter(category__in=selected_categories)
        return queryset

    def value(self):
        values = self.used_parameters.get(self.parameter_name, None)
        return values.split(',') if values else []

    def choices(self, changelist):
        values = self.value()
        base_url = self.request.get_full_path().split('?')[0]
    
        for lookup, title in self.lookups(self.request, changelist.model_admin):
            current_selection = list(values)
    
            if lookup in current_selection:
                current_selection.remove(lookup)
            else:
                current_selection.append(lookup)
    
            new_query_part = f"{self.parameter_name}=" + ','.join([quote(lookup) for lookup in current_selection])
    
            if new_query_part:
                new_query_string = f"{base_url}?{new_query_part}"
            else:
                new_query_string = base_url
    
            yield {
                'selected': lookup in values,
                'query_string': new_query_string,
                'display': title,
                'lookup': lookup,
            }
