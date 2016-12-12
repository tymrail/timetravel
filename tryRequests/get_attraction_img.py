import json
import random

import requests
import time
from bs4 import BeautifulSoup


for i in range(1, 7):
    r = requests.get("http://harbin.cncn.com/jingdian/1-" + str(i) + "-0-0.html")

    bs = BeautifulSoup(r.text, 'lxml')

    attraction_list = bs.find_all("div", {"class": "city_spots_list"})

    for attraction in attraction_list:
        # place_list = list()
        # m = month_place['data-month']
        for a in attraction.find_all("a", {"class": "pic"}):
            img = a.find("img", {"class": "lazy"})["data-original"]
            attraction_title = a.find("div", {"class": "title"}).find("b").string
            ir = requests.get(img)
            img_src = 'beijing/' + attraction_title + '.jpg'
            if ir.status_code == 200:
                open(img_src, 'wb').write(ir.content)

            print(attraction_title + ' done')

        time.sleep(random.uniform(0.5, 0.8))

