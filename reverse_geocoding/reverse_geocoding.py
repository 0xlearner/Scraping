import requests
import json
import time

class ReverseGeoCoding:
    #base url
    base_url = 'https://nominatim.openstreetmap.org/reverse'

    data = []

    def fetch(self, lat, lon):
        # Headers
        headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0'}

        # Params
        params = {
            'format': 'jsonv2',
            'lat': lat,
            'lon': lon
        }
        #HTTP GET Request
        res = requests.get(url=self.base_url, params=params, headers=headers)
        print(f'HTTP GET Request to URL: {res.url} | Status code: {res.status_code}')

        if res.status_code == 200:
            return res
        else:
            return None

    def parse(self, res):
        given_lat = json.dumps(res['lat'])
        given_lon = json.dumps(res['lon'])
        name = json.dumps(res['name'])
        road = json.dumps(res['address']['road'])
        state_district = json.dumps(res['address']['state_district'])
        state = json.dumps(res['address']['state'])
        postalcode = json.dumps(res['address']['postcode'])
        country = json.dumps(res['address']['country'])
        country_code = json.dumps(res['address']['country_code'])
        #print(name)
        self.data.append({
            'given_lat': given_lat,
            'given_lon': given_lon,
            'Name': name,
            'Road': road,
            'State_District': state_district,
            'State': state,
            'Postcode': postalcode,
            'Country': country,
            'Country_Code': country_code
        })

        #print(json.dumps(data, indent=2))

    def store_data(self):
        # write json data
        with open('reverse_geocode.json', 'w') as output_file:
            output_file.write(json.dumps(self.data, indent=2))

    def run(self):
        # load coordinates
        cords = ''

        with open('coordinates.txt', 'r') as coordinates:
            for line in coordinates.read():
                cords += line

        cords = cords.split('\n')
        
        for cordinate in cords:
            lon = cordinate.split(',')[0].strip()
            lat = cordinate.split(',')[1].strip()

            # Make HTTP Request to Nominatim API
            res = self.fetch(lat, lon)

            self.parse(res.json())

            time.sleep(2)

            self.store_data()
            #print(lat, lon)

if __name__ == '__main__':
    reverse_geocoder = ReverseGeoCoding()
    reverse_geocoder.run()