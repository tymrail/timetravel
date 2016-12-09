from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from django.contrib.auth.models import User
from authonline.models import MyUser, City, Attraction, Route

from django.contrib.auth.decorators import user_passes_test, login_required


def index(request):
    user = request.user if request.user.is_authenticated() else None
    user_n = user.username
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


def show_routes(request):
    user = request.user if request.user.is_authenticated() else None
    all_route_list = Route.objects.all().order_by("-route_popular")[:21]

    all_route = get_routes(all_route_list)

    # if request.method == 'GET' and request.GET('user_name'):
    #     my_route = Route.objects.get(route_owner__username__exact=request.GET.get('user_name'))

    state = 'out'
    my_route = list()
    if user is not None:
        my_route_list = Route.objects.get(route_owner__username__exact=user.username)
        my_route = get_routes(my_route_list)
        state = 'in'

    content = {
        'user': user,
        'active_menu': 'show_routes',
        'all_route': all_route,
        'my_route': my_route,
        'state': state,
    }

    return render(request, 'travel/show_routes.html', content)


def get_routes(routes_list):
    all_route = list()
    for rt in routes_list:
        sight_list = rt.get_route_detail()
        sights = list()
        for s in sight_list:
            sights.append(Attraction.objects.get(attraction_id__exact=s))
        route_temp = {
            'route_info': rt,
            'route_sights': sights,
        }
        all_route.append(route_temp)
    return all_route


@login_required
def create_or_update_route(request):
    user = request.user if request.user.is_authenticated() else None
    if user is None:
        return HttpResponseRedirect(reverse('homepage'))

    if request.method == 'POST':
        if request.POST('route_id'):
            update_route = Route.objects.filter(route_id__exact=request.POST.get('route_id'))
            update_route.update(
                route_name=request.POST.get('route_name'),
            )
            update_route.set_route_detail(request.POST.getlist('route_detail_list'))
        else:
            user_add_to = User.objects.get(username__exact=user.username)
            new_route = Route(
                route_name=request.POST.get('route_name', ''),
                route_creator=user_add_to,
            )
            route_detail_list = request.POST.getlist('route_detail_list', [])
            new_route.set_route_detail(route_detail_list)
            new_route.save()
            new_route.route_owner.add(user_add_to)

    elif request.method == 'GET':
        if request.GET.get('option') == 'create':

            route_exact = Route.objects.filter(route_id__exact=request.GET.get('route_id'))
            route = get_routes(route_exact)[0]

# TODO 修改对旅游路线的增删查改功能，配套前端
# TODO 组队功能
# TODO 针对拥有相同旅游路线的/旅游路线拥有相同关键字的人进行队友推荐


@login_required
def quit_route(request):
    if request.method == 'GET' and request.GET('route_id'):
        route = Route.objects.filter(route_id__exact=request.GET.get('route_id'))

    return HttpResponseRedirect(reverse('personal'))


@login_required
def personal(request):
    user = request.user if request.user.is_authenticated() else None
    if user is None:
        return HttpResponseRedirect(reverse('login'))

    content = {
        'user': user,
        'active_menu': 'personal',
    }

    return render(request, 'authonline/personal.html', content)

