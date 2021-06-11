import requests
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'en-US,en;q=0.5',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'X-Requested-With': 'XMLHttpRequest',
    'Origin': 'https://lifebridgecapital.com',
    'Connection': 'keep-alive',
    'Referer': 'https://lifebridgecapital.com/podcast/',
    'Sec-GPC': '1',
    'TE': 'Trailers',
}

data = {
'action': 'gdlr_core_post_ajax', 
'settings[category][]': 'podcast', 
'settings[tag]': '', 
'settings[num-fetch]': '9', 
'settings[pagination]': 'load-more', 
'settings[paged]': '1', 
'option[name]': 'paged', 

}

session = requests.Session()

for page in range(0, 55):
    data['option[value]'] = str(page + 1)
    response = session.post('https://lifebridgecapital.com/wp-admin/admin-ajax.php', headers=headers, data=data)
    links = [a['href'] for a in BeautifulSoup(response.text, 'lxml').select('h3 > a')]
    for link in links:
        link = 'https://lifebridgecapital.com/' + "".join(link.split('/')[3:-1])
        #print(link)
        response = session.get(link.replace("\\", '/'))
        page = BeautifulSoup(response.text, 'lxml')
        title = page.find('title').text
        print(f'Title: {title}, Link: {link}')
