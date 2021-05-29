import requests
from bs4 import BeautifulSoup
import json
import csv
import time

class GoogleScraper:

    #https://www.google.com/search?q=linux+mint&sxsrf=ALeKk02ztIsY6EB3HVbo7g626v952mTSkQ%3A1622280192142&source=hp&ei=AAiyYNP5BYf6-QbEwqWoBA&iflsig=AINFCbYAAAAAYLIWECpmfblTkNZHzDo3BA3gMdDtJqhE&oq=linux+mint&gs_lcp=Cgdnd3Mtd2l6EAMyBAgjECcyAggAMgIIADICCAAyAggAMgIIADICCAAyAggAMgIIADIFCAAQiwM6CAgAELEDEIMBOgUIABCxAzoICAAQsQMQiwM6AgguUMIKWM8oYIQraANwAHgAgAGoA4gBrSKSAQYzLTEwLjKYAQCgAQGqAQdnd3Mtd2l6uAED&sclient=gws-wiz&ved=0ahUKEwjT-c3UyO7wAhUHfd4KHURhCUUQ4dUDCAY&uact=5
    #https://www.google.com/search?q=linux+mint&sxsrf=ALeKk03iDomfnSeAymiQi-IsrndB4JL_Kg:1622287229557&ei=fSOyYNyzIbHDmAWX3LzACg&start=10&sa=N&ved=2ahUKEwic5qnw4u7wAhWxIaYKHRcuD6gQ8tMDegQIARA0&biw=692&bih=654

    base_url = 'https://www.google.com/search'

    pagination_params = {
        'q': 'linux mint', 
        'sxsrf': 'ALeKk03iDomfnSeAymiQi-IsrndB4JL_Kg:1622287229557', 
        'ei': 'fSOyYNyzIbHDmAWX3LzACg', 
        'start': '', 
        'sa': 'N', 
        'ved': '2ahUKEwic5qnw4u7wAhWxIaYKHRcuD6gQ8tMDegQIARA0',
        'biw': '692',
        'bih': '654'
    }

    intitial_params = {
        'sxsrf': 'ALeKk02ztIsY6EB3HVbo7g626v952mTSkQ%3A1622280192142', 
        'source': 'hp', 
        'ei': 'AAiyYNP5BYf6-QbEwqWoBA', 
        'q': '', 
        'iflsig': 'AINFCbYAAAAAYLIWECpmfblTkNZHzDo3BA3gMdDtJqhE', 
        'oq': '', 
        'gs_lcp': 'Cgdnd3Mtd2l6EAMyBAgjECcyAggAMgIIADICCAAyAggAMgIIADICCAAyAggAMgIIADIFCAAQiwM6CAgAELEDEIMBOgUIABCxAzoICAAQsQMQiwM6AgguUMIKWM8oYIQraANwAHgAgAGoA4gBrSKSAQYzLTEwLjKYAQCgAQGqAQdnd3Mtd2l6uAED', 
    }

    headers = {
        'accept': '*/*', 
        'accept-language': 'en-US,en;q=0.9', 
        'cache-control': 'no-cache', 
        'pragma': 'no-cache', 
        'referer': 'https://www.google.com/', 
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"', 
        'sec-ch-ua-mobile': '?0', 
        'sec-fetch-dest': 'empty', 
        'sec-fetch-mode': 'cors', 
        'sec-fetch-site': 'same-origin', 
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36', 'x-client-data': 'CIy2yQEIorbJAQjBtskBCKmdygEI+MfKAQjnissBCNGaywEIjZ3LAQioncsBCKagywEIraDLAQjAoMsBCNzyywEIp/PLARiS9csB'
        }

    results = []

    def fetch(self, query, page):
        self.intitial_params['q'] = query
        if not page:
            params = self.intitial_params
        else:
            params = self.pagination_params
            params['start'] = str(page * 10)
            params['q'] = query

        # print(json.dumps(params, indent=2))
        # return
        response = requests.get(self.base_url, params=params, headers=self.headers)
        print(f'HTTP GET Request to URL: {response.url} | Status Code: {response.status_code}')
        return response
        #print(response)

    def parse(self, html):

        content = BeautifulSoup(html, 'lxml')
        titles = [title.text for title in content.find_all('h3', {'class': 'LC20lb DKV0Md'})]
        links = [link.next_element['href'] for link in content.find_all('div', {'class': 'yuRUbf'})]
        description = [desc.text for desc in content.find_all('div', {'class': 'IsZvec'})]
        #print(description, len(description))

        for index in range(0, len(titles)):
            self.results.append({
                'Title': titles[index],
                'Links': links[index],
                'Description': description[index]
            })

            #print(json.dumps(item, indent=2))

    def store_response(self,response):
        if response.status_code == 200:
            print('Saving Response to "res.html"')
            with open('res.html', 'w', encoding='utf-8') as html_file:
                html_file.write(response.text)

            print('Done!')

        else:
            print('Bad Response')

    def load_response(self):
        html = ''
        with open('res.html', 'r', encoding='utf-8') as html_file:
            for line in html_file.read():
                html += line

        return html


    def write_csv(self):
        if len(self.results):
            print('Writing Results to CSV')
            with open('Google_Search_Results.csv', 'w', newline='', encoding='utf-8') as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames=self.results[0].keys())
                writer.writeheader()

                for row in self.results:
                    writer.writerow(row)
            print('Stored results in "Google_Search_Results.csv"')

    def run_crawler(self):

        for page in range(0, 5):
            if page:
                response = self.fetch('linux mint', page)
                self.parse(response.text)
            else:
                response = self.fetch('linux mint', page)
                self.parse(response.text)

            time.sleep(5)
        # response = self.fetch('linux mint')
        # self.store_response(response)
        # html = self.load_response()
        # self.parse(html)
        self.write_csv()


if __name__ == '__main__':
    scraper = GoogleScraper()
    scraper.run_crawler()