from bs4 import BeautifulSoup as bs
import requests
import csv
import json
import time

class ZillowScraper:
    results = []

    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', 
        'accept-encoding': 'gzip, deflate, br', 
        'accept-language': 'en-US,en;q=0.9', 
        'cache-control': 'no-cache', 
        'cookie': 'zguid=23|%2424de1c44-3cce-49ae-8e2d-cfb76b05882a; zgsession=1|df7eeb41-b1f5-46f3-8bdf-79290f694f7b; JSESSIONID=6CEDDD27FAF7C5DF046F3CC285956918; search=6|1624180076880%7Cregion%3Dny%26rect%3D50.62214%252C-68.327143%252C23.705962%252C-125.374896%26disp%3Dmap%26mdm%3Dauto%26p%3D2%26pt%3Dpmf%252Cpf%26fs%3D1%26fr%3D0%26mmm%3D1%26rs%3D0%26ah%3D0%09%0943%09%09%09%09%09%09; AWSALB=HJXkpcOMkgGbc4Us8Ez6RX9jb9bThSAw4B11ng7BgOG/LYJr6U+kMA1FJtmjR4I6Tippk4oSTZmolmTRBcoISvyhd+N1Lof4FUrigdCf7qZ039mDlt39OhIrlc4J; AWSALBCORS=HJXkpcOMkgGbc4Us8Ez6RX9jb9bThSAw4B11ng7BgOG/LYJr6U+kMA1FJtmjR4I6Tippk4oSTZmolmTRBcoISvyhd+N1Lof4FUrigdCf7qZ039mDlt39OhIrlc4J',
        'pragma': 'no-cache', 
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"', 
        'sec-ch-ua-mobile': '?0', 
        'sec-fetch-dest': 'document', 
        'sec-fetch-mode': 'navigate', 
        'sec-fetch-site': 'same-origin', 
        'sec-fetch-user': '?1', 
        'upgrade-insecure-requests': '1', 
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'
    }

    def fetch(self, url,params):
        print(f'HTTP GET request to URL: {url}', end='')
        res = requests.get(url, params=params, headers=self.headers)
        print(f' | Status Code: {res.status_code}')

        return res

    def save_response(self, res):
        with open('res.html', 'w', encoding='utf-8') as html_file:
            html_file.write(res)

    def load_response(self):
        html = ''

        with open('res.html', 'r', encoding='utf-8') as html_file:
            for line in html_file:
                html += line

        return html

    def parse(self, html):
        content = bs(html, 'html.parser')
        content_area = content.find('script', {'data-zrr-shared-data-key': 'mobileSearchPageStore'}).contents[0].strip("'<>!-")
        json_format = json.loads(content_area)
        data_end_point = json_format['cat1']['searchResults']['listResults']
        #print(content_area)

        

        for listing in data_end_point:

            try:
                BrokerPhone = listing['brokerPhone']
            except:
                BrokerPhone = 'N/A'

            self.results.append({
                'listing_ID': listing['id'],
                'status_Text': listing['statusText'],
                'Address': listing['address'],
                'Bedrooms': listing['beds'],
                'Bathrooms': listing['baths'],
                'Lat': listing['latLong']['latitude'],
                'Long': listing['latLong']['longitude'],
                'LivingArea': listing['area'],
                'HomeType': listing['hdpData']['homeInfo']['homeType'],
                'BrokerName': listing['brokerName'],
                'BrokerPhone': BrokerPhone,
                'Detail_URL': listing['detailUrl'],
                'Image': listing['imgSrc'],
                'Price': listing['price']
                })
        #print(json.dumps(data_end_point, indent=2))
        #print(self.results)
    def to_csv(self):
        with open('zillow.csv', 'w', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=self.results[0].keys())
            writer.writeheader()

            for row in self.results:
                writer.writerow(row)

            print('Stored results to "zillow.csv"')

    def run(self):
        for page in range(1, 5):
            params = {
                'searchQueryState': '{"pagination":{"currentPage":%s},"usersSearchTerm":"new york","mapBounds":{"west":-102.84035200000001,"east":-48.69972700000001,"south":25.056818000006064,"north":56.59039373644349},"mapZoom":4,"regionSelection":[{"regionId":43,"regionType":2}],"isMapVisible":false,"filterState":{"ah":{"value":true},"sort":{"value":"globalrelevanceex"}},"isListVisible":true}'%page
        }

        #res = self.fetch('https://www.zillow.com/ny/2_p/', params)
        #html = self.load_response()
            res = self.fetch('https://www.zillow.com/new-york-ny/fsbo/2_p/', params)
            self.parse(res.text)
            time.sleep(2)
        
        self.to_csv()



if __name__ == '__main__':
    scraper = ZillowScraper()
    scraper.run()