from os import link
from requests_html import HTMLSession
import csv

# Set up
s = HTMLSession()

def get_product_links(page):
    links = []
    url = f'https://themes.woocommerce.com/storefront/product-category/clothing/page/{page}'
    r = s.get(url)
    # print(r.status_code)
    products = r.html.find('ul.products li')
    for item in products:
        links.append(item.find('a', first=True).attrs['href'])
    return links

def parse_product(url):    
    r = s.get(url)
    title = r.html.find('h1.product_title.entry-title', first=True).text.strip()
    price = r.html.find('p.price', first=True).text.strip().replace('\n','')
    try:
        sku = r.html.find('span.sku', first=True).text.strip()
    except AttributeError as err:
        sku = "None"
    cat = r.html.find('span.posted_in a', first=True).text.strip()
    product = {
        'title': title,
        'price': price,
        'sku': sku,
        'cat': cat,
    }
    return product

def save_to_csv(results):
    keys = results[0].keys()
    with open('products.csv', 'w') as f:
        dict_writer = csv.DictWriter(f, keys)
        dict_writer.writeheader()
        dict_writer.writerows(results)

def main():
    results = []
    for x in range(1,5):   
        print("Getting page: ", x) 
        links = get_product_links(x)
        for link in links:
            results.append(parse_product(link))
        print(len(results))
    save_to_csv(results)

if __name__ == '__main__':
    main()