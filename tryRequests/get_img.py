import json
import random

import requests
import time
from bs4 import BeautifulSoup

r = requests.get("http://www.cncn.com/place/")

bs = BeautifulSoup(r.text, 'lxml')

months_place = bs.find_all("div", {"class": "img_ali"})

for month_place in months_place:
    place_list = list()
    m = month_place['data-month']
    for a in month_place.find_all("a"):
        href = a["href"]
        city_e = href[7:-9]
        img = a.find("img")["src"]
        province = a.find("p", {"class": "t"}).find("span").string
        city = a.find("p", {"class": "t"}).text.replace(province,"")
        intro = a.find("p", {"class": "c"}).string
        a_dic = {
            "month": m,
            "city_title": city_e,
            "city_name": city,
            "province": province,
            "intro": intro,
        }
        place_list.append(a_dic)
        ir = requests.get(img)
        img_src = 'month_place/' + city_e + '.jpg'
        if ir.status_code == 200:
            open(img_src, 'wb').write(ir.content)

        print(city_e + ' done')

    json_src = 'month_place/' + m + '.json'

    with open(json_src, 'w', encoding='utf-8') as file:
        result_json = json.dumps(place_list, skipkeys=True, ensure_ascii=False)
        file.write(result_json)

    time.sleep(random.uniform(0.5, 0.8))