from django.shortcuts import render

from django.http import HttpResponse
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import pandas as pd
import re



def convert_price(price):
    prices = re.findall(r'\$[\d.]+', price)
    converted_prices = [float(p[1:]) for p in prices]
    final_price = max(converted_prices) if len(converted_prices) > 1 else converted_prices[0]
    return int(final_price)

def run_playwright(search_term):
    modified_text = search_term.replace(" ", "+")

    with sync_playwright() as playwright:
        browser = playwright.firefox.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        page.set_default_timeout(100000)

        page.goto(f"https://www.ebay.com/sch/i.html?_from=R40&_trksid=p2380057.m570.l1313&_nkw={modified_text}&_sacat=0")
        html = page.content()
        soup = BeautifulSoup(html, 'html.parser')

        items = soup.find('ul', class_='srp-results srp-list clearfix').find_all('li', class_='s-item s-item__pl-on-bottom')
        first_10 = items[:10]

        titles = [x.find('div', class_='s-item__title').text.strip() for x in first_10]
        prices = [convert_price(x.find('span', class_='s-item__price').text.strip()) for x in first_10]

        seller_types = [x.find('span', class_='s-item__etrs-text').text.strip() if x.find('span', class_='s-item__etrs-text') else 'Not Available' for x in first_10]
        product_links = [x.find('a', class_='s-item__link').get('href') for x in first_10]
        image_link = [x.find('div', class_='s-item__image-wrapper image-treatment').img['src'] for x in first_10]

        data = {'Title': titles, 'Price': prices, 'Seller Type': seller_types, 'Product Link': product_links, 'Image URL': image_link, 'Website': 'www.ebay.com'}
        
        
        df = pd.DataFrame(data)

        context.close()
        browser.close()
        return data
        
data = run_playwright('Kirkland')

print(data)