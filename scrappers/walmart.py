import subprocess
from playwright.sync_api import Playwright, sync_playwright
subprocess.run(["playwright", "install"])


from bs4 import BeautifulSoup
import pandas as pd
import re

pattern = r'(\d+)current price'


def generate_walmart_search_url(search_term):
        search_words = search_term.split()
        url = "https://www.walmart.com/search?q=" + '+'.join(search_words)
        return url

# executable_path = '/usr/bin/chromium', args = ['--disable-gpu'],ignore_default_args=["--mute-audio"], 
def run_playwright(search_term):
    data_list = []
    
    link  = generate_walmart_search_url(search_term)


    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless = False)
        context = browser.new_context()
        page = context.new_page()
        page.set_default_timeout(100000)

        page.goto(link)
        page.set_default_timeout(100000)
        html = page.content()
        
        s = BeautifulSoup(html, 'html.parser')
        divs = s.find('div',class_='flex flex-wrap w-100 flex-grow-0 flex-shrink-0 ph2 pr0-xl pl4-xl mt0-xl').find_all('div',class_='mb0 ph1 pa0-xl bb b--near-white w-25')
        un_sponsored = [x for x in divs if 'Sponsored' not in x.text]
        
        first_10 = un_sponsored[:10] 


        for i in first_10:
            title = i.find('span', class_='w_V_DM').text
            try:
                price = i.find('div', class_='flex flex-wrap justify-start items-center lh-title mb1').find('span',class_='f2').text
                cents = i.find('div', class_='flex flex-wrap justify-start items-center lh-title mb1').find_all('span',class_='f6 f5-l')[1].text
                full_price = price+'.'+cents 
            except:
                price_text = i.find('div',class_='flex flex-wrap justify-start items-center lh-title mb1 mb0').text
                match = re.search(pattern, price_text)
                if match:
                    full_price = match.group(1)
                    full_price = int(full_price)/100
                else:
                    full_price = 'None'


            try:
                seller_type = i.find('div', class_='h2 relative mb2').text
            except:
                seller_type = 'None'
            try:
                prod_link = 'https://www.walmart.com'+i.find('div', class_='sans-serif mid-gray relative flex flex-column w-100 hide-child-opacity').find('a').get('href')
            except:
                prod_link = 'None'

            try:
                img_tag = i.find('img')
                srcset_attribute = img_tag['srcset']
                srcset_attribute = srcset_attribute.split(', ')
                srcset_attribute = srcset_attribute[-1].replace(' 2x', '')
            except:
                img_tag = i.find('div',class_='relative overflow-hidden').find('img')
                if img_tag:
                    srcset_attribute = img_tag['src']
                else:
                    srcset_attribute = 'None'
                

            kw = search_term
            data = {'Title': title, 'Price': full_price, 'Seller_Type': seller_type, 'Product_Links': prod_link, 'Image_URLs': srcset_attribute, 'Website': 'www.walmart.com','KW':kw}
            data_list.append(data)

        context.close()
        browser.close()
        
        return data_list

# data = run_playwright('Kirkland Minoxidil')
# print(data)



        
    
