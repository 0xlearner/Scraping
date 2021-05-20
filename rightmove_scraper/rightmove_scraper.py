import requests
from bs4 import BeautifulSoup
import csv

class RightMoveScraper:

    results = []

    def fetch(self, url):
        print(f'HTTP GET request to URL: {url}', end='')
        response = requests.get(url)
        print(f' | Status code: {response.status_code}')

        return response

    def parse(self, html):
        content = BeautifulSoup(html, 'lxml')
        titles = [title.text.strip() for title in content.find_all('h2', {'class':'propertyCard-title'})]
        addresses = [address['content'] for address in content.find_all('meta', {'itemprop':'streetAddress'})]
        description = [description.text for description in content.find_all('span', {'itemprop':'description'})]
        price = [price.text.strip() for price in content.find_all('div', {'class':'propertyCard-priceValue'})]
        dates = [date.text.split(' ')[-1] for date in content.find_all('span', {'class':'propertyCard-branchSummary-addedOrReduced'})]
        seller = [seller.text for seller in content.find_all('span', {'class':'propertyCard-branchSummary-branchName'})]
        image = [image['src'] for image in content.find_all('img', {'itemprop':'image'})]
        #print(image)

        for index in range(0, len(titles)):
            self.results.append({
                'title': titles[index],
                'address': addresses[index],
                'description': description[index],
                'price': price[index],
                'dates': dates[index],
                'seller': seller[index],
                'image': image[index]
            })

    def to_csv(self):
        with open('rightmove.csv', 'w') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=self.results[0].keys())
            writer.writeheader()

            for row in self.results:
                writer.writerow(row)

            print('Stored results to "rightmove.csv"')

    def run(self):
        for page in range(0, 5):
            index = page * 24
            url = 'https://www.rightmove.co.uk/property-for-sale/find.html?locationIdentifier=REGION%5E93917&index=' + str(index) + '&propertyTypes=&mustHave=&dontShow=&furnishTypes=&keywords='

            response = self.fetch(url)
        
            self.parse(response.text)
        
        self.to_csv()

if __name__ == '__main__':
    scraper = RightMoveScraper()
    scraper.run()