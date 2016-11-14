from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from authonline.models import MyUser, City, Attraction


def index(request):
    user = request.user if request.user.is_authenticated() else None
    city_reclist = City.objects.filter(city_is_rec=True)
    attraction_reclist = Attraction.objects.filter(attraction_is_rec=True)
    content = {
        'active_menu': 'index',
        'city_reclist': city_reclist,
        'attraction_reclist': attraction_reclist,
        'user': user,
    }

    return render(request, 'travel/index.html', content)


def cities(request):
    user = request.user if request.user.is_authenticated() else None
    if request.method == 'GET' and request.GET.get('show_all') == 'true':
        city_list = City.objects.all()
        state = 'all_city'
    else:
        city_list = City.objects.filter(city_is_rec=True)
        state = 'rec_city'

    content = {
        'user': user,
        'state': state,
        'active_menu': 'cities',
        'cities': city_list,
    }

    return render(request, 'travel/cities.html', content)


def attractions(request):
    user = request.user if request.user.is_authenticated() else None
    # TODO: ugly code. try next time.
    if request.method == 'GET':
        city_id = request.GET.get('city_id')
        city = City.objects.filter(city_id__exact=city_id)
        attraction_list = Attraction.objects.filter(attraction_city__city_id__exact=city_id)
        state = 'city_attraction'

        content = {
            'user': user,
            'active_menu': 'attractions',
            'state': state,
            'city': city[0],
            'attraction_list': attraction_list,
        }
    else:
        attraction_list = Attraction.objects.filter(attraction_is_rec=True)
        state = 'rec_attraction'

        content = {
            'user': user,
            'active_menu': 'attractions',
            'state': state,
            'attraction_list': attraction_list,
        }

    return render(request, 'travel/attractions.html', content)


def attraction_info(request):
    user = request.user if request.user.is_authenticated() else None
    if request.method == 'GET':
        attraction_id = request.GET.get('attraction_id')
        attraction_detail = Attraction.objects.filter(attraction_id=attraction_id)[0]
        mapxy_list = attraction_detail.attraction_mapxy.split(',')
        mapxy = {
            'x': float(mapxy_list[0]),
            'y': float(mapxy_list[1]),
        }
    else:
        return HttpResponseRedirect(reverse('homepage'))
    content = {
        'user': user,
        'active_menu': 'attraction_info',
        'attraction_info': attraction_detail,
        'mapxy': mapxy,
    }

    return render(request, 'travel/attraction_info.html', content)



