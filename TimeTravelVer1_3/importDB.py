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

if __name__ == "__main__":
    load_data()
