from django.shortcuts import render
from .forms import URLForm
from .models import Product
import time
import requests
from bs4 import BeautifulSoup
from decimal import Decimal, InvalidOperation

def fetch_links_from_sitemap(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'xml')
    links = []

    for url_tag in soup.find_all('url'):
        loc_tag = url_tag.find('loc')
        if loc_tag:
            links.append(loc_tag.get_text())
    
    return links

def clean_price(price_str):
    cleaned_price = ''.join(c for c in price_str if c.isdigit() or c == '.')
    return cleaned_price

def fetch_product_details_hydrosan(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    }
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')

        name_element = soup.select_one('section.heading.inside.to-left .title')
        name = name_element.get_text(strip=True) if name_element else "Unknown Product"

        price_element = soup.select_one('.core_scbRaty')
        if price_element:
            price_str = price_element.get('data-price', '0.00')
            cleaned_price = clean_price(price_str)
            try:
                price = Decimal(cleaned_price)
            except InvalidOperation:
                price = Decimal('0.00')
        else:
            price = Decimal('0.00')

        stock_element = soup.select_one('span.hidden[data-parameter-value="availability_amount_number"]')
        if stock_element:
            stock_str = stock_element.get('data-parameter-default-value', '1')
            try:
                stock = int(stock_str)
            except ValueError:
                stock = 1
        else:
            stock = 1

        category_elements = soup.select('div.breadcrumbs-wrapper ul li')[1:]  
        categories = " -> ".join([el.get_text(strip=True) for el in category_elements])


        website = url

        product, created = Product.objects.update_or_create(
            website=website,
            defaults={'name': name, 'price': price, 'stock': stock, 'category': categories, 'shop': 'Hydrosan'}
        )
        return product
    except Exception as e:
        print(f"Error processing {url}: {e}")
        return None
    
def fetch_product_details_mazurspa(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    }
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')

        name_element = soup.select_one('h1.product_title')
        name = name_element.get_text(strip=True) if name_element else "Unknown Product"

        price_element = soup.select_one('.summary.entry-summary .woocommerce-Price-amount')
        if price_element:
            price_str = price_element.get_text(strip=True).replace(',', '.')
            cleaned_price = clean_price(price_str)
            try:
                price = Decimal(cleaned_price)
            except InvalidOperation:
                price = Decimal('0.00')
        else:
            price = Decimal('0.00')

        stock_element = soup.select_one('.stock-strong')
        if stock_element and stock_element.get_text(strip=True) == "W magazynie":
            stock = 1
        else:
            stock = 0

        category_elements = soup.select('span.posted_in a')
        categories = " -> ".join([el.get_text(strip=True) for el in category_elements])

        website = url

        product, created = Product.objects.update_or_create(
            website=website,
            defaults={'name': name, 'price': price, 'stock': stock, 'category': categories, 'shop': 'mazurspa'}
        )
        return product
    except Exception as e:
        print(f"Error processing {url}: {e}")
        return None

def fetch_product_details_spapartsvortex(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    }
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        print(url)
        body_class = soup.find('body').get('class', [])
        if 'catalog-product-view' not in body_class:
            return None

        name_element = soup.select_one('.product-name h1')
        name = name_element.get_text(strip=True) if name_element else "Unknown Product"

        stock_element = soup.select_one('.stockQty span')
        if stock_element:
            stock_str = stock_element.get_text(strip=True).split()[0]
            try:
                stock = int(stock_str)
            except ValueError:
                stock = 0
        else:
            stock = 0

        category_elements = soup.select('.breadcrumbs li a')[1:]  # Adjust the selector based on the actual HTML structure
        categories = " > ".join([el.get_text(strip=True) for el in category_elements])

        website = url

        product, created = Product.objects.update_or_create(
            website=website,
            defaults={'name': name, 'price': Decimal('0.00'), 'stock': stock, 'category': categories, 'shop': 'SpaPartsVortex'}
        )
        return product
    except Exception as e:
        print(f"Error processing {url}: {e}")
        return None

def fetch_all_products():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    }
    base_url = 'https://www.spapartsvortex.eu'
    category_url = f'{base_url}/categories'
    
    response = requests.get(category_url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    main_category_links = [a['href'] for a in soup.select('a.product-image')]

    for main_category_link in main_category_links:
        response = requests.get(main_category_link, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        sub_category_links = [a['href'] for a in soup.select('a.product-image')]

        for sub_category_link in sub_category_links:
            response = requests.get(sub_category_link, headers=headers)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            product_links = [a['href'] for a in soup.select('a.product-image')]

            for product_link in product_links:
                fetch_product_details_spapartsvortex(product_link)

def crawl_sitemap(url, fetch_details_function):
    product_links = fetch_links_from_sitemap(url)
    all_products = []

    if product_links:
        for link in product_links:  
            product = fetch_details_function(link)
            if product:
                all_products.append(product)
            time.sleep(1)  

    return all_products

def fetch_categories(request):
    form = URLForm()
    if request.method == 'POST':
        form = URLForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data['url']
            if 'hydrosan' in url:
                fetch_details_function = fetch_product_details_hydrosan
            elif 'mazurspa' in url:
                fetch_details_function = fetch_product_details_mazurspa
            elif 'spapartsvortex' in url:
                fetch_details_function = fetch_product_details_spapartsvortex
            else:
                fetch_details_function = None

            if fetch_details_function:
                products = crawl_sitemap(url, fetch_details_function)
                product_names = [product.name for product in products]
            else:
                product_names = []
        else:
            product_names = []
    else:
        product_names = []

    return render(request, 'products/fetch_categories.html', {'form': form, 'categories': product_names})
