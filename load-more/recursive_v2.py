import requests
from bs4 import BeautifulSoup
import csv
import time


url = "https://lifebridgecapital.com/podcast/"

soup = BeautifulSoup(requests.get(url).content, "html.parser")
tag_links = [a["href"] for a in soup.select(".tagcloud a")]
titles = []
article_links = []
tag_words = []
scraped_data = []

for link in tag_links:
    while True:
        print(link)
        print("-" * 80)

        soup = BeautifulSoup(requests.get(link).content, "html.parser")

        for title in soup.select("h3 a"):
            titles.append(title.text)
            print(title.text)
        
        for article_link in soup.select("h3 a"):
            article_links.append(article_link['href'])
            print(article_link['href'])
        
        tags = soup.select("div.infinite-page-caption")[0]
        for i in range(len(soup.select("h3 a"))):
        	tag_words.append(tags.text)
        	print(tags.text)

        #print(tag_words)

        next_link = soup.select_one("a.next")
        if not next_link:
            break

        link = next_link["href"]
def get(list, index, default=None):
    try:
        return list[index]
    except IndexError:
        return default
for index in range(len(titles)):
        scraped_data.append({
            'Title': titles[index],
            'Tags': get(tag_words, index),
            'Links': article_links[index]
        })

# print(scraped_data)

with open('tag-based-scraped-data.csv', 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=scraped_data[0].keys())

        writer.writeheader()

        for row in scraped_data:
            writer.writerow(row)

print(len(tag_words))
print(len(titles))
print(len(article_links))