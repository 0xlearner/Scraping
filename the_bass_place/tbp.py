from requests_html import HTMLSession
import csv
import time


def get_links(url):
    global _session
    _request = _session.get(url)
    items = _request.html.find('li.product-grid-view.product.sale')
    links = []
    for item in items:
        links.append(item.find('a', first=True).attrs['href'])
    return links


def get_product(link):
    global _session
    _request = _session.get(link)
    title = _request.html.find('h2', first=True).full_text
    price = _request.html.find('span.woocommerce-Price-amount.amount bdi')[1].full_text
    sku = _request.html.find('span.sku', first=True).full_text
    categories = _request.html.find('span.posted_in', first=True).full_text.replace('Categories:', "").strip()
    brand = _request.html.find('span.posted_in')[1].full_text.replace('Brand:', "").strip()
    product = {
        'Title': title,
        'Price': price,
        'SKU': sku,
        'Categories': categories,
        'Brand': brand
    }
    return product


if __name__ == '__main__':
    results = []
    for page in range(1, 4):
        url = 'https://www.thebassplace.com/product-category/basses/4-string/'
        if page == 1:
            parse_url = url
        else:
            parse_url = f'https://www.thebassplace.com/product-category/basses/4-string/page/{page}/'
        print(parse_url)
    
        _session = HTMLSession()
        links = get_links(parse_url)

        for link in links:
            product = get_product(link)
            results.append(product)
            time.sleep(1)
            
    with open('on_sale_bass.csv', 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=results[0].keys())
        writer.writeheader()
        for row in results:
            writer.writerow(row)