import requests
import json
import time

class GeoCode:
    base_url = 'https://nominatim.openstreetmap.org/search'

    #results
    data = []

    def fetch(self, address):
        #string query parameters
        params = {
            'q': address,
            'format': 'geocodejson'
        }

        res = requests.get(url=self.base_url, params=params)
        print(f'HTTP GET Request to URL: {res.url} | Status code: {res.status_code}')

        if res.status_code == 200:
            return res
        else:
            return None

    def parse(self, res):
        
        label = json.dumps(res['features'][0]['properties']['geocoding']['label'], indent=2)
        long = json.dumps(res['features'][0]['geometry']['coordinates'][0], indent=2)
        lat = json.dumps(res['features'][0]['geometry']['coordinates'][1], indent=2)
        #print(label)
        try:
            name = json.dumps(res['features'][0]['properties']['geocoding']['name'], indent=2)
        except:
            name = None
        # retrieved data
        self.data.append({
            'Name': name,
            'Address': label,
            'Longitude': long,
            'Latitude': lat 
        })

        #print(json.dumps(data, indent=2))

    def store_data(self):
        with open('data.json', 'w') as output_file:
            output_file.write(json.dumps(self.data, indent=2))

    def run(self):

        addresses = ''

        with open('addresses.txt', 'r') as address:
            for line in address.read():
                addresses += line

        addresses = addresses.split('\n')

        for address in addresses:
            res = self.fetch(address).json()
            self.parse(res)


            time.sleep(2)

        #store_data
        self.store_data()


if __name__ == '__main__':
    geocoder = GeoCode()
    geocoder.run()