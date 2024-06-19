from django.core.management.base import BaseCommand
from scrapper.views import fetch_product_details_hydrosan, fetch_product_details_mazurspa, crawl_sitemap, fetch_all_products

class Command(BaseCommand):
    help = 'Fetch products from Hydrosan and Mazur Spa'

    def add_arguments(self, parser):
        parser.add_argument(
            '--site',
            type=str,
            help='Specify which site to fetch products from (options: hydrosan, mazurspa, mazurspa2, spapartsvortex)'
        )

    def handle(self, *args, **kwargs):
        site = kwargs['site']
        
        sites = {
            'hydrosan': ('https://hydrosan.eu/sitemap-produkty.xml', fetch_product_details_hydrosan),
            'mazurspa': ('https://mazurspa.pl/product-sitemap.xml', fetch_product_details_mazurspa),
            'mazurspa2': ('https://mazurspa.pl/product-sitemap2.xml', fetch_product_details_mazurspa),
            'spapartsvortex': (None, fetch_all_products),
        }

        if site:
            if site in sites:
                url, fetch_function = sites[site]
                self.stdout.write(f'Fetching products from {site.capitalize()}...')
                if url is None:
                    fetch_function()
                else:
                    crawl_sitemap(url, fetch_function)
                self.stdout.write(self.style.SUCCESS(f'Successfully fetched products from {site.capitalize()}'))
            else:
                self.stdout.write(self.style.ERROR(f'Unknown site: {site}'))
        else:
            for site_name, (url, fetch_function) in sites.items():
                self.stdout.write(f'Fetching products from {site_name.capitalize()}...')
                if url is None:
                    fetch_function()
                else:
                    crawl_sitemap(url, fetch_function)

            self.stdout.write(self.style.SUCCESS('Successfully fetched products from all sites'))