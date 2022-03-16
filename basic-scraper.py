from requests_html import HTMLSession

# Set up
s = HTMLSession()

def get_product_links(page):
    links = []
    url = f'https://themes.woocommerce.com/storefront/product-category/clothing/page/{page}'
    r = s.get(url)
    print(r.status_code)
    products = r.html.find('ul.products li')

    for item in products:
        links.append(item.find('a', first=True).attrs['href'])
    return links

page1 = get_product_links(1)
print(page1)