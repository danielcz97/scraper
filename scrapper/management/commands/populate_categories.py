from django.core.management.base import BaseCommand
from scrapper.models import Product, Category

class Command(BaseCommand):
    help = 'Populates unique categories from products into Category model and updates products with category_id'

    def handle(self, *args, **options):
        unique_categories = set()
        for product in Product.objects.all():
            unique_categories.add((product.category, product.website))

        category_map = {}
        for category_name, website_name in unique_categories:
            category, created = Category.objects.get_or_create(name=category_name, website=website_name)
            category_map[(category_name, website_name)] = category.id

        for product in Product.objects.all():
            category_id = category_map.get((product.category, product.website))
            if category_id:
                product.category_id = category_id
                product.save()

        self.stdout.write(self.style.SUCCESS(f'Successfully added {len(unique_categories)} categories and updated products.'))
