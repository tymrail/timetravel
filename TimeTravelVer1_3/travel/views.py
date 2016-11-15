from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from authonline.models import MyUser, City, Attraction


def index(request):
    user = request.user if request.user.is_authenticated() else None
    if request.method == 'POST':
        search_key = request.POST.get('search_key')
        if search_key == 'city':
            city_seo = request.POST.get('search_seo')
            city_result = list()
            city_search = City.objects.filter(city_name=city_seo)
            city_dict = {
                'city': city_search,
                # 'city_attractions': city_attractions,
            }
            display = {
                'city_result': city_dict,
            }
            state = 'search_city'
        elif search_key == 'attraction':
            attraction_search = Attraction.objects.filter(attraction_title__contains=search_key)
            display = {
                'attraction_search': attraction_search,
            }
            state = 'search_attraction'
        else:
            return HttpResponseRedirect(reverse('homepage'))
    else:
        city_reclist = City.objects.filter(city_is_rec=True)
        attraction_reclist = Attraction.objects.filter(attraction_is_rec=True)
        display = {
            'city_reclist': city_reclist,
            'attraction_reclist': attraction_reclist,
        }
        state = 'index'

    content = {
        'active_menu': 'index',
        'user': user,
        'display': display,
        'state': state,
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
            'attraction_list': attraction_list[0:20],
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
        'state': 'attraction_info',
    }

    return render(request, 'travel/attraction_info.html', content)



