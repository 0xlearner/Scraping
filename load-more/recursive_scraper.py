import requests
from bs4 import BeautifulSoup
import csv


url = "https://lifebridgecapital.com/podcast/"
    
soup = BeautifulSoup(requests.get(url).content, "html.parser")
tag_links = [a["href"] for a in soup.select(".tagcloud a")]
    
scraped_data = []
    
for link in tag_links:
    while True:
        print(link)
        print("-" * 80)
    
        soup = BeautifulSoup(requests.get(link).content, "html.parser")
        t = [tag.text for tag in soup.select('div.infinite-page-caption')]
        
        for title in soup.select("h3 a"):
            article = {
                'title': title.text,
                'article_link': title['href'],
                'tags': t
            }
            print(article)
            scraped_data.append(article)
        
        
        print()
        # print(tag_words)
    
        next_link = soup.select_one("a.next")
        if not next_link:
            break
    
        link = next_link["href"]
    
    
with open('tag-based-scraped-data.csv', 'w', newline='', encoding='utf-8') as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=scraped_data[0].keys())
    writer.writeheader()
    for row in scraped_data:
        writer.writerow(row)