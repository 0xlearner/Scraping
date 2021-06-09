import requests
from bs4 import BeautifulSoup
import json

base_url = 'https://en.wikipedia.org/wiki/List_of_postal_codes_in_Germany'

# make HTTP GET Request to base_url
res = requests.get(base_url)




# '''
# # store response to local html
# # with open('res.html', 'w', encoding='utf-8') as html_file:
# #     html_file.write(res.text)

# # read local HTML response to debug selectors
# html = ''
# with open('res.html', 'r', encoding='utf-8') as html_file:
#     for line in html_file.read():
#         html += line


# '''
# parse response
content = BeautifulSoup(res.text, 'lxml')

# postcodes list

postcodes = []



# data extraction logic
for ul in content.find_all('ul')[19:220]:
    for li in ul.find_all('li'):
        if li.text.split()[-1] != '\u2013':
        # extract postcodes
            item = {
                'postcodes': li.text.split()[0],
                'region': li.text.split()[-1]
            }

            # fix the unicode symbols
            if '\u2013' in item['postcodes']:
                item['postcodes'] = item['postcodes'].split('\u2013')[0]

            postcodes.append(item)

        #print(json.dumps(postcodes, indent=2))

#convert postcodes to string
postcodes = json.dumps(postcodes, indent=2)
#print(postcodes)

# write postcodes to JSON format
with open('german_postcodes.json', 'w', encoding='utf-8') as json_file:
    json_file.write(postcodes)


#print results
print(postcodes)
print(f'Written {len(json.loads(postcodes))} postcodes to "german_postcodes.json"')