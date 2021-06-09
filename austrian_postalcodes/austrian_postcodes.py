import requests
from bs4 import BeautifulSoup

# make HTTP GET request

response = requests.get('https://en.wikipedia.org/wiki/List_of_postal_codes_in_Austria')

# parse content

content = BeautifulSoup(response.text, 'lxml')

# extract postcodes

postcodes = [postcodes.text for postcodes in content.find_all('li') 
            if ' - ' in postcodes.text
            ]

# filter postcodes

postcodes = [postcode.split()[0] for postcode in postcodes
            if len(postcode.split()) == 3 or
            len(postcode.split()) == 4]

# write output to txt file

with open('austrian_postcodes.txt', 'a', encoding='utf-8') as file:
    for postcode in postcodes:
        file.write(postcode + '\n')