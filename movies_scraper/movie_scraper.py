import requests
from bs4 import BeautifulSoup
import csv
import json
import os.path
import time
class MovieScraper:

    base_url = 'https://en.hkcinema.ru/films/?pg='
    
    def fetch(self, url):
        print(f'HTTP GET Request to URL: {url}', end='')
        response = requests.get(url)
        print(f' | Status code: {response.status_code}')

        return response

    def parse(self, html):
        content = BeautifulSoup(html, 'lxml')
        titles = [title.find('span', {'class': 'red'}).text for title in content.find_all('div', {'class': 'top-block'})]
        countries = [country.find('img', {'class': 'flag'}).get('title') for country in content.find_all('div', {'class': 'top-block'})]
        release_years = [year.find('div', {'class': 'film-persons'}).text.split('\n')[2] for year in content.find_all('div', {'class': 'middle-block'})]
        directors = [director.find('div', {'class': 'film-persons'}).text.split('\n')[7] for director in content.find_all('div', {'class': 'middle-block'})]
        starring = ['\n'.join([star.text for star in stars.find_all('div', {'data-role': 'links'})]) for stars in content.find_all('div', {'class': 'middle-block'})]
        #print(starring[0].split('\n')[1], len(starring))

        for index in range(0, len(titles)):

            genre = starring[index].split('\n')[1]
            #print(starring[index].split('\n')[5])

            try:
                cast = starring[index].split('\n')[5]

            except:
                cast = ''

            if 'martial arts' in genre:
                #print(genre)
                #print(starring[index].split('\n')[5])
                item = {
                    'Title': titles[index],
                    'Country': countries[index],
                    'Released': release_years[index],
                    'Directors': directors[index],
                    'Genre': genre,
                    'Starring': cast
                }

                #print(json.dumps(item, indent=2))
                self.to_csv(item)

            else:
                continue


    def to_html(self, response):
        print('Writing html_file')
        with open('res.html', 'w', encoding='utf-8') as html_file:
            html_file.write(response.text)

    def from_html(self):
        with open('res.html', 'r', encoding='utf-8') as html_file:
            html = ''

            print('Reading html_file')
            for line in html_file.read():
                html += line

        return html

    def to_csv(self, item):
        movies_csv = os.path.isfile('movies.csv')

        with open('movies.csv', 'a', newline='', encoding='utf-8') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=item.keys())

            if not movies_csv:
                writer.writeheader()

            writer.writerow(item)

            with open('movies.csv', 'r', newline='', encoding='utf-8') as duplicate_csv, open('martial_arts_movies.csv', 'w', newline='', encoding='utf-8') as out_file:
                seen = set()
                for line in duplicate_csv:
                    if line in seen: continue

                    seen.add(line)
                    out_file.write(line)

    def run_crawler(self):

        for page in range(1, 5):
            next_page = self.base_url + str(page)
            response = self.fetch(next_page)
            self.parse(response.text)
            time.sleep(2)
        #response = self.fetch(self.base_url)
        html = self.from_html()
        self.parse(html)

if __name__ == '__main__':
    scraper = MovieScraper()
    scraper.run_crawler()