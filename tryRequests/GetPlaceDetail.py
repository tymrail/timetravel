import json
import requests
from bs4 import BeautifulSoup
import re
import time
import random

with open('placelink.txt', 'r') as link_file:
    AllPlacesLinks = list(link_file)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'
}

for link in AllPlacesLinks:
    try:
        link = link.replace('\n', '')
        time.sleep(random.uniform(0.5, 1))
        base = requests.get(link, headers=headers)
        base_soup = BeautifulSoup(base.text, 'html.parser')
        page_count_str = base_soup.select('.page_con .text')
        if len(page_count_str) == 0:
            page_count = 0
        else:
            page_count = int(re.findall(r'\d+', page_count_str[0].string)[0])
            if page_count >= 12:
                page_count = 12

        place_title = base_soup.select('.city_top strong span')[0].string

        attraction_list = list()

        for i in range(page_count):
            time.sleep(random.uniform(0.5, 1))
            search = requests.get(link + '1-' + str(i + 1) + '-0-0.html', headers=headers)
            search_soup = BeautifulSoup(search.text, 'html.parser')
            place_info = search_soup.select('.city_spots .city_spots_list ul li')

            for j in range(len(place_info)):
                # 景点具体网址
                attraction_href = place_info[j].select('.pic')[0].get('href')

                # 景点名称
                attraction_title = place_info[j].select('.pic .title b')[0].string

                # 景点门票价格
                attraction_price_html = place_info[j].select('.num .price b')
                if len(attraction_price_html) == 0:
                    attraction_price = ''
                else:
                    attraction_price = attraction_price_html[0].string

                time.sleep(random.uniform(0.5, 1))
                attraction_detail = requests.get(attraction_href, headers=headers)
                attraction_detail_soup = BeautifulSoup(attraction_detail.text, 'html.parser')

                # 景点经纬度
                attraction_mapxy_url = attraction_detail_soup.select('.map250 img')
                if len(attraction_mapxy_url) == 0:
                    continue
                attraction_mapxy = attraction_mapxy_url[0]['src'].split('markers=')[1]

                attraction_rate = attraction_detail_soup.select('.type em')[0].string

                # 景点描述
                # attraction_type_key = place_info[j].select('.type dt')
                # attraction_type_item = place_info[j].select('.type dd')
                # attraction_introduce = attraction_detail_soup.select('.type .introduce dd')[0].string

                # 景点酒店
                hotels_key = attraction_detail_soup.select('.list_hotel .txt .text_con p')
                hotels_item = attraction_detail_soup.select('.list_hotel .txt .text_con .price b')

                # attraction_intro = dict()
                # for key, item in zip(attraction_type_key, attraction_type_item):
                #     attraction_intro[key.string] = item.string

                attraction_hotels = list()
                for key, item in zip(hotels_key, hotels_item):
                    hotel_dict = {
                        'hotel_name': key.string,
                        'hotel_price': item.string,
                    }
                    attraction_hotels.append(hotel_dict)

                attraction_information = {
                    # 'attraction_intro': attraction_introduce,
                    'attraction_mapxy': attraction_mapxy,
                    'attraction_hotel': attraction_hotels,
                    'attraction_price': attraction_price,
                }

                attraction_dict = {
                    'attraction_name': attraction_title,
                    'attraction_information': attraction_information,
                }

                attraction_list.append(attraction_dict)
                print(place_title + ' ' + 'total: ' + str(page_count) + ',' + str(i) + ' ' + str(j) + ' completed')
        place_dict = {
            'place_name': place_title,
            'place_attractions': attraction_list,
        }

        json_src = 'places/' + place_title + '.json'

        with open(json_src, 'w', encoding='utf-8') as file:
            result_json = json.dumps(place_dict, skipkeys=True, ensure_ascii=False)
            file.write(result_json)

        print(place_title + ' completed')
    except Exception as e:
        print('Fail to get ' + str(link))
        print(str(e))
        with open('failure.txt', 'w', newline="\n") as error_file:
            error_file.writelines(str(link))
            error_file.writelines('  ')
            error_file.writelines(str(e))
        pass
        time.sleep(random.uniform(0.5, 1))
