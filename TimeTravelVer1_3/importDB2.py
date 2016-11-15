import os
import os.path
import django
import json

rootdir = "D:\\month_place"

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "TimeTravelVer1_3.settings")

django.setup()


def load_data():
    for parent, dirnames, filenames in os.walk(rootdir):
        from authonline.models import City
        for filename in filenames:
            file_path = os.path.join(parent, filename)
            with open(file_path, 'rb') as file:
                data_json = file.read().decode('utf8')
                data = json.loads(data_json, encoding="utf8")

                for city in data:
                    title = city['city_title'].capitalize()
                    City.objects.get_or_create(city_title=title)
                    city_iexact = City.objects.filter(city_title=title)
                    city_iexact.update(
                        city_name=city['city_name'],
                        city_rec_month=int(city['month']),
                        city_province=city['province'],
                        city_img_src=city['city_title'] + ".jpg",
                        city_is_rec=True,
                        city_intro=city['intro'],
                    )

                print('done')

if __name__ == "__main__":
    load_data()
