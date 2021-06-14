import requests
from bs4 import BeautifulSoup
import re


# target url
url = 'https://en.wikipedia.org/wiki/List_of_postal_codes_in_Italy'

# make HTTP GET request to the target url
response = requests.get(url)

# parse HTML document
content = BeautifulSoup(response.text, 'lxml')
#print(content)

# extract postcodes table
table = content.find("table")
#print(table.text)

# extract table rows
rows = table.find_all('tr')
#print(rows)

# extract row columns
cols = [
    [   col.text.strip('\n') 
        for col in 
        row.find_all('td')
    ]
    for row in 
    rows
]

# init raw postcodes list
raw_data = []

# init postcodes list
postcodes =[]

for col in cols[1:]:
    # capital towns postcodes
    raw_data.append(col[3])
    # CAP other towns
    raw_data.append(col[4])

# loop over postcodes list
for item in raw_data:
    # extracting capital towns postcodes
    if len(item.split()) == 1 and item != '-':
        postcodes.append(item)

# extract raw postcodes ranges
ranges = re.findall(r'(\d+ to \d+)', '\n'.join(raw_data))
# print(ranges)

# loop over raw postcodes ranges
for item in ranges:
    from_range = int(item.split(' to ')[0])
    to_range = int(item.split(' to ')[1])

    # loop over current range
    for postcode in range(from_range, to_range + 1):
        postcodes.append(str(postcode).zfill(5))

# extract comma seperated postcodes
sets = re.findall(r'(\d+)?,(\d+)', '\n'.join(raw_data))
sets = ','.join([','.join(item) for item in sets]).replace(',,', ',')
sets = sets.split(',')
# print(sets)

# loop over postcode sets
for postcode in sets:
    postcodes.append(postcode)


# extract all the left sets
other_sets = re.findall(r'(\d+ \(.+\), \d+ \(.+\))', '\n'.join(raw_data))

# loop over left sets
for item in other_sets:
    raw = [text.split() for text in item.split(',')]

    # loop over raw list
    for postcode in raw:
        postcodes.append(postcode[0])

# extracting 471xx (47121-47122) (Forlì), 475xx (47521-47522) (Cesena)
left_one = re.findall(r'(\d+xx \(\d+-\d+\))', '\n'.join(raw_data))
left_one = ','.join([','.join(item for item in left_one)])
left_one = left_one.split()
#print(left_one[1:])
for item in left_one[1:]:
    raw_text = [text.split() for text in item.split(',')]
    raw_text = ''.join([''.join(text) for text in raw_text[0]])
    raw_text = raw_text.split('-')
    from_range = int(raw_text[0].replace('(', ''))
    to_range = int(raw_text[1].replace(')', ''))
    
    for postcode in range(from_range, to_range + 1):
        postcodes.append(str(postcode))


# loop over postcodes
for postcode in postcodes:
    # write postcodes to txt file
    with open('italian_postcodes.txt', 'a') as file:
        file.write(postcode + '\n')
