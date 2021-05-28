from bs4 import BeautifulSoup
import requests
import csv
import time


results = []

def fetch(url):
    #print('HTTP GET: %s | Status code: %s' % (url.url, url.status_code))
    response = requests.get(url)
    #print(f' | Status code: {response.status_code}')

    return response
def parse(response):
    #print(f'HTTP GET: {response.url} | Status code: {response.status_code}')

    content = BeautifulSoup(response.text, 'lxml')
    

    #Extract Data Fields
    # for a in content.find(class_='blog-posts clear').find_all('a'):
    #     if a['href'][26:30] != year:
            # # The slice 26:30 contains the year in the articles' urls
    labels = content.findAll('div', {'class': 'item-label'})
    story_date = [[tag for tag in date][1] for date in labels]
    story_title = [title.text for title in content.find_all('h2', {'class': 'home-title'})]
    story_link = [story_link['href'] for story_link in content.find(class_='blog-posts clear').find_all('a') if story_link['href'] != year]
    link = [i for n, i in enumerate(story_link) if i not in story_link[:n]]
    story_author = [[tag for tag in author][2].text.strip('\n')[1:] for author in labels]
        
    for index in range(0, len(story_date)):
        results.append({
            'date': story_date[index],
            'title': story_title[index],
            'link': link[index],
            'author': story_author[index]
        })

def export_to_csv(filename):
    with open(filename, 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=results[0].keys())

        writer.writeheader()

        for row in results:
            writer.writerow(row)

    with open(filename, 'r', newline='', encoding='utf-8') as duplicate_csv, open('clean_results.csv', 'w', newline='', encoding='utf-8') as out_file:
        seen = set()
        for line in duplicate_csv:
            if line in seen: continue

            seen.add(line)
            out_file.write(line)


if __name__ == '__main__':

    baseURL = 'https://thehackernews.com/search/label/'

    categories = ['data%20breach', 'Cyber%20Attack', 'Vulnerability', 'Malware']

    years = ['2018', '2019']

    for category in categories:
        for year in years:
            url = baseURL + category + f'?updated-max={year}-12-31T23:59:59-00:00'
            res = fetch(url)
            html_parsing = parse(res)
            export_to_csv('thn.csv')
            time.sleep(2)



    