import requests
from bs4 import BeautifulSoup
import csv
import time

class LightupScraper:

    results = []

    def fetch(self, url):
        print(f'HTTP GET request to URL: {url}', end='')
        res = requests.get(url)
        print(f' | Status Code: {res.status_code}')

        return res

    def save_response(self, res):
        with open('res.html', 'w') as html_file:
            html_file.write(res)

    def load_response(self):
        html = ''

        with open('res.html', 'r') as html_file:
            for line in html_file:
                html += line

            return html

    def parse(self, html):


        content = BeautifulSoup(html, 'lxml')
        titles = [title.text.strip() for title in content.find_all('h4', {'class': 'card-title ols-card-title'})]
        links = [link.find('a')['href'] for link in content.find_all('h4', {'class': 'card-title ols-card-title'})]
        skus = [sku.text for sku in content.find_all('span', {'class': 'productView-info-value ols-card-text--sku'})]
        mpn = [mpn.text.split(':')[-1].strip() for mpn in content.find_all('span', {'class': 'productView-info-name mpn-label ols-card-text--mpn'})]
        details = [ul.find_all('li') for ul in content.find_all('ul', {'class': 'ols-card-text__list'})]
        brand = [''.join([brand.text for brand in detail if 'Brand:' in brand.text]).split(':')[-1].strip() for detail in details]
        base = [''.join([base.text for base in detail if 'Base Type:' in base.text]).split(':')[-1].strip() for detail in details]
        life_hours = [''.join([life_hour.text for life_hour in detail if 'Life Hours:' in life_hour.text]).split(':')[-1].strip() for detail in details]
        lumens = [''.join([lumen.text for lumen in detail if 'Lumens:' in lumen.text]).split(':')[-1].strip() for detail in details]
        warrantys = [''.join([warranty.text for warranty in detail if 'Warranty:' in warranty.text]).split(':')[-1].strip() for detail in details]
        wattages = [''.join([wattage.text for wattage in detail if 'Wattage:' in wattage.text]).split(':')[-1].strip() for detail in details]
        features = [feature.text.split() for feature in content.find_all('span', {'class': 'ols-card-text__list--features'})]
        prices = [price.text for price in content.find_all('span', {'class': 'price price--withoutTax'})]
        #prices_pc = [price_pc.text for price_pc in content.find_all('div', {'class': 'price price--withoutTax price-per--item'})]
        #print(prices)



        for feature in features:
            feat = feature

        for index in range(0, len(titles)):
            # Append scraped item to results list
            self.results.append({
                'Title': titles[index],
                'Link': links[index],
                'MPN': mpn[index],
                'SKU': skus[index],
                'Base': base[index],
                'Wattage': wattages[index],
                'Life Hours': life_hours[index],
                'Lumens': lumens[index],
                'Brand': brand[index],
                'Warranty': warrantys[index],
                'Features': feat[index],
                'Price': prices[index]
            })

    def to_csv(self):

        with open('lightup.csv', 'w', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=self.results[0].keys())
            writer.writeheader()

            for row in self.results:
                writer.writerow(row)

            print('Exported results to lightup.csv')

    def run(self):
        
        page_num = 3

        for page in range(1, page_num + 1):
            base_url = 'https://www.lightup.com/standard-household-lighting.html?p='
            base_url += str(page)
            res = self.fetch(base_url)
            self.parse(res.text)
            #time.sleep(30)

        self.to_csv()
        # html = self.load_response()
        # self.parse(html)
        #self.save_response(html.text)


if __name__ == '__main__':
    scraper = LightupScraper()
    scraper.run()