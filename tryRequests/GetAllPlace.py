import requests
from bs4 import BeautifulSoup

r = requests.get('http://www.cncn.com/place/')

r_soup = BeautifulSoup(r.text, 'html.parser')

places = r_soup.select('#gn .li a')

with open('placelink.txt', 'w') as link_file:
    for place in places:
        link_file.write(place['href'] + '/jingdian/')
        link_file.write('\n')

with open('placename.txt', 'w') as name_file:
    for place in places:
        name_file.write(place.string)
        name_file.write('\n')
