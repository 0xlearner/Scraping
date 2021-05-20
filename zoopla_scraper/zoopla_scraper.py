import requests
import json
import csv
import time
from bs4 import BeautifulSoup as bs

class ZooplaScraper:

    results = []

    def fetch(self, url):
        print(f'HTTP GET request to URL: {url}', end='')
        res = requests.get(url)
        print(f' | Status code: {res.status_code}')

        return res

    def parse(self, html):
        content = bs(html, 'html.parser')
        content_array = content.select('script[id="__NEXT_DATA__"]')
        content_dict = json.loads(content_array[0].string)
        content_details = content_dict['props']['initialProps']['pageProps']['regularListingsFormatted']

        for listing in content_details:
            self.results.append ({
                'listing_id': listing['listingId'],
                'name_title': listing['title'],
                'names': listing['branch']['name'],
                'addresses': listing['address'],
                'agent': 'https://zoopla.co.uk' + listing['branch']['branchDetailsUri'],
                'phone_no': listing['branch']['phone'],
                'picture': listing['image']['src'],
                'prices': listing['price'],
                'Listed_on': listing['publishedOn'],
                'listing_detail_link': 'https://zoopla.co.uk' + listing['listingUris']['detail']


            })

    def to_csv(self):
        
        with open('zoopla.csv', 'w') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=self.results[0].keys())
            writer.writeheader()

            for row in self.results:
                writer.writerow(row)

            print('Stored results to "zoopla.csv"')

    def run(self):

        for page in range(1, 5):
            url = 'https://www.zoopla.co.uk/for-sale/property/london/?page_size=25&q=London&radius=0&results_sort=newest_listings&pn='
            url += str(page)
            res = self.fetch(url)
            self.parse(res.text)
            time.sleep(2)
        self.to_csv()

if __name__ == '__main__':
    scraper = ZooplaScraper()
    scraper.run()