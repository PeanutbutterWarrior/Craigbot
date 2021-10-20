import urllib.request
import urllib.parse
from bs4 import BeautifulSoup


def get_url(url):
    with urllib.request.urlopen(url) as response:
        return response.read()


location_areas = get_url('https://www.homedepot.com/l/storeDirectory')
location_areas_soup = BeautifulSoup(location_areas, features='html.parser')
location_areas_urls = [tag['href'] for tag in location_areas_soup.find_all('a', class_='store-directory__state-link--n43yd')]

addresses = []
for url in location_areas_urls:
    page_soup = BeautifulSoup(get_url(url), features='html.parser')
    for address_group in page_soup.find_all('ul', class_='store-directory__store-details--n43yd'):
        line1, line2, *_ = address_group.find_all('li')
        addresses.append((line1.contents[0], line2.contents[0]))


with open('home_depot_locations.txt', 'w+') as file:
    for line1, line2 in addresses:
        file.write(f'{line1}:{line2}\n')


parameters = {'apiKey': '397c7d10898e496f9226f07d0febeb31'}

for line1, line2 in addresses:
    parameters['text'] = f'{line1}, {line2}'
    querystring = urllib.parse.urlencode(parameters)
    response = get_url('https://api.geoapify.com/v1/geocode/search?' + querystring)