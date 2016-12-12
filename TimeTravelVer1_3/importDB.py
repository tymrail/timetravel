import os
import os.path
import django
import json

rootdir = "D:\\places"

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "TimeTravelVer1_3.settings")

django.setup()


def load_data():
    for parent, dirnames, filenames in os.walk(rootdir):
        from authonline.models import Attraction, City
        for filename in filenames:
            # print("parent is:" + parent)
            # print("filename with full path :" + os.path.join(parent, filename))
            file_path = os.path.join(parent, filename)
            with open(file_path, 'rb') as file:
                data_json = file.read().decode('utf8')
                data = json.loads(data_json, encoding="utf8")
                city_last = City.objects.all().last()
                if city_last is None:
                    city_new_id = 0
                else:
                    city_new_id = city_last.city_id + 1

                City.objects.create(
                    city_id=city_new_id,
                    city_title=data['place_name'],
                )
                for a in data['place_attractions']:

                    if a['attraction_information']['attraction_price'] == '':
                        price = '0'
                    else:
                        price = int(a['attraction_information']['attraction_price'])

                    attraction_last = Attraction.objects.all().last()
                    if attraction_last is None:
                        attraction_new_id = 0
                    else:
                        attraction_new_id = attraction_last.attraction_id + 1

                    Attraction.objects.create(
                        attraction_id=attraction_new_id,
                        attraction_title=a['attraction_name'],
                        attraction_price=price,
                        attraction_mapxy=a['attraction_information']['attraction_mapxy'],
                        attraction_city=City.objects.get(city_id__exact=city_new_id),
                    )

                print('done')


def print_province_data():
    from authonline.models import City, Attraction
    all_city = City.objects.all()
    province_set = set()

    for city in all_city:
        province_set.add(city.city_province)

    province_list = sorted(list(province_set))

    # print(province_set)
    with open('province_info.txt', 'a') as file:
        i = 0
        for province in province_list:
            file.write('{code: \'' + str(3000 + i) + '\', address: \'' + province + '\'},')
            file.write('\n')
            i += 1


def set_city_data():
    from authonline.models import City, Attraction

    all_city = City.objects.all()
    province_set = set()

    for city in all_city:
        province_set.add(city.city_province)

    province_list = sorted(list(province_set))
    province_index_list = list()
    for j in range(len(province_list)):
        province_index_list.append(j + 93000)

    all_city_index_with_province = list()
    all_city_name_with_province = list()

    for k in range(len(province_index_list)):
        city_list = City.objects.filter(city_province=province_list[k])
        city_index_list = list()
        city_name_list = list()

        for v in range(len(city_list)):
            city_index_list.append(city_list[v].city_id + 83000)
            city_name_list.append(city_list[v].city_name)

        all_city_index_with_province.append(city_index_list)
        all_city_name_with_province.append(city_name_list)

    with open('province.txt', 'a') as file:
        for i in range(len(province_index_list)):
            file.write(str(province_index_list[i]) + ': {\n')
            for j in range(len(all_city_index_with_province[i])):
                file.write('\t' + str(all_city_index_with_province[i][j])
                           + ':\'' + all_city_name_with_province[i][j] + '\',\n')
            file.write('},\n')


if __name__ == "__main__":
    from authonline.models import City, Attraction

    all_city = City.objects.all()
    province_set = set()

    for city in all_city:
        province_set.add(city.city_province)

    province_list = sorted(list(province_set))
    province_index_list = list()
    for j in range(len(province_list)):
        province_index_list.append(j + 93000)

    all_city_index_with_province = list()
    all_city_name_with_province = list()

    for k in range(len(province_index_list)):
        city_list = City.objects.filter(city_province=province_list[k])

        for v in range(len(city_list)):
            all_city_index_with_province.append(city_list[v].city_id + 83000)
            all_city_name_with_province.append(city_list[v].city_name)

    all_attraction_index_with_city = list()
    all_attraction_name_with_city = list()

    for k in range(len(all_city_index_with_province)):
        attraction_list = Attraction.objects.filter(
            attraction_city__city_name=all_city_name_with_province[k])
        attraction_index_list = list()
        attraction_name_list = list()
        for v in range(len(attraction_list)):
            attraction_index_list.append(attraction_list[v].attraction_id)
            attraction_name_list.append(attraction_list[v].attraction_title)

        all_attraction_index_with_city.append(attraction_index_list)
        all_attraction_name_with_city.append(attraction_name_list)

    with open('city.txt', 'a', encoding='utf-8') as file:
        for i in range(len(all_city_index_with_province)):
            file.write(str(all_city_index_with_province[i]) + ': {\n')
            for j in range(len(all_attraction_index_with_city[i])):
                file.write('\t' + str(all_attraction_index_with_city[i][j])
                           + ':\'' + all_attraction_name_with_city[i][j] + '\',\n')
            file.write('},\n')

    # with open('province.txt', 'a') as file:
    #     for i in range(len(province_index_list)):
    #         file.write(str(province_index_list[i]) + ': {\n')
    #         for j in range(len(all_city_index_with_province[i])):
    #             file.write('\t' + str(all_city_index_with_province[i][j])
    #                        + ':\'' + all_city_name_with_province[i][j] + '\',\n')
    #         file.write('},\n')

    # 120000: {
    #     120100: '天津市'
    # },

    # print(province_set)
    # with open('province_info.txt', 'a') as file:
    #     i = 0
    #     for province in province_list:
    #         file.write('{code: \'' + str(3000 + i) + '\', address: \'' + province + '\'},')
    #         file.write('\n')
    #         i += 1

# {code: '340000', address: '安徽省'},
# if __name__ == '__main__':
#     from authonline.models import City
#     non_province_city = City.objects.filter(city_province__contains="直辖市")
#     print(non_province_city)
