from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt

from authonline.models import MyUser, City, Attraction, Team, TeamRelation, Route, RouteRelation
from blog.models import Blog
from django.contrib.auth.decorators import user_passes_test, login_required


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
        blog_4_city = Blog.objects.filter(blog_city=city)

        content = {
            'user': user,
            'active_menu': 'attractions',
            'state': state,
            'city': city[0],
            'blog_4_city': blog_4_city,
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
        relate_route = list()
        routes_all = Route.objects.all()
        for route in routes_all:
            route_lists = route.get_route_detail()
            if int(attraction_id) in route.get_route_detail():
                relate_route.append(route)
    else:
        return HttpResponseRedirect(reverse('homepage'))
    content = {
        'user': user,
        'active_menu': 'attraction_info',
        'attraction_info': attraction_detail,
        'mapxy': mapxy,
        'state': 'attraction_info',
        'relate_routes': relate_route,
    }

    return render(request, 'travel/attraction_info.html', content)


def show_routes(request):
    user = request.user if request.user.is_authenticated() else None
    all_route_list = Route.objects.all().order_by("-route_popular")[:21]

    all_route = get_routes(all_route_list)

    # if request.method == 'GET' and request.GET('user_name'):
    #     my_route = Route.objects.get(route_owner__username__exact=request.GET.get('user_name'))

    user_create_routes = Route.objects.filter(route_creator__username__exact=user.username)

    user_create_routes_list = list()

    for uor in user_create_routes:
        route_attractions = list()
        for i in uor.get_route_detail():
            route_attractions.append(Attraction.objects.filter(attraction_id__exact=i)[0])
        user_create_routes_list.append({
            'route_self': uor,
            'route_attractions': route_attractions,
        })

    user_own_routes_relations = RouteRelation.objects.filter(route_relation_owner__username__exact=user.username)

    user_own_routes_list = list()
    for ur in user_own_routes_relations:
        # user_own_routes_list.append(Route.objects.filter(route_id__exact=ur.route_relation_id)[0])
        route_own_l = Route.objects.filter(route_id__exact=ur.route_relation_id)
        if len(route_own_l) > 0:
            route_own = route_own_l[0]
        route_own_attractions = list()
        for i in route_own.get_route_detail():
            route_own_attractions.append(Attraction.objects.get(attraction_id__exact=int(i)))
        user_own_routes_list.append({
            'route_self': route_own,
            'route_attractions': route_own_attractions,
        })

    content = {
        'user': user,
        'active_menu': 'show_routes',
        'all_route': all_route,
        'route_create_list': user_create_routes_list,
        'route_own': user_own_routes_list,
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


@csrf_exempt
@login_required
def create_route(request):
    user = request.user if request.user.is_authenticated() else None
    if user is None:
        return HttpResponseRedirect(reverse('login'))

    state = 'unknown'

    if request.method == 'POST':
        new_route = Route(
            route_name=request.POST.get('route_name', ''),
            route_keywords=request.POST.get('route_keywords', ''),
            route_creator=user,
        )
        route_detail_string = request.POST.get('route_detail_string', '')
        route_detail_list = route_detail_string.split(',')
        new_route.set_route_detail(str_list_to_int(route_detail_list))
        new_route.save()

        # add relation row
        new_route_relation = RouteRelation(
            route_relation_id=new_route.route_id,
            route_relation_owner=user,
        )
        new_route_relation.save()
        new_route.route_owner.add(new_route_relation)
        state = 'success'
        return HttpResponseRedirect(reverse('homepage'))
    content = {
        'state': state,
    }

    return render(request, 'travel/create_route.html', content)


def route_detail(request):
    user = request.user if request.user.is_authenticated() else None
    if request.method == 'GET' and 'route_id' in request.GET:
        route_exact = Route.objects.filter(route_id__exact=request.GET.get('route_id', ''))[0]
        route_attractions = list()
        for i in route_exact.get_route_detail():
            route_attractions.append(Attraction.objects.filter(attraction_id__exact=i)[0])
        updateble = (route_exact.route_creator == user)
        is_owner = (user in User.objects.filter(route_relation__route_relation_id__exact=route_exact.route_id))

        content = {
            'user': user,
            'route': route_exact,
            'route_attractions': route_attractions,
            'updateble': updateble,
            'is_owner': is_owner,
        }

        if is_owner is True:
            rec_teams = Team.objects.filter(team_route__exact=route_exact)\
                .exclude(team_member__team_relation_member__username=user.username)
            content['rec_teams'] = rec_teams
        return render(request, 'travel/route_detail.html', content)
    else:
        return HttpResponseRedirect(reverse('personal'))


@login_required
def operate_route(request):
    user = request.user if request.user.is_authenticated() else None
    if request.method == 'GET' and request.GET.get('operate') == 'update':
        updating_route = Route.objects.filter(route_id__exact=request.GET.get('route_id'))
        if request.GET('route_name'):
            updating_route.update(route_name=request.GET.get('route_name'))
        if request.GET('route_detail'):
            updating_route.set_route_detail(request.GET.get('route_detail'))

    elif request.method == 'GET' and request.GET.get('operate') == 'delete':
        Route.objects.filter(route_id__exact=request.GET.get('route_id')).delete()
    else:
        route_operate = Route.objects.filter(route_id__exact=request.GET.get('route_id'))
        content = {
            'route_operate': route_operate,
            'state': 'show',
            'active_menu': 'operate_route',
        }
        return render(request, 'travel/operate.html', content)
    return HttpResponseRedirect(reverse('show_routes'))


@login_required
def join_route(request):
    user = request.user if request.user.is_authenticated() else None
    if request.method == 'GET' and 'route_id' in request.GET:
        route_join = Route.objects.filter(route_id__exact=request.GET.get('route_id'))
        new_route_relation = RouteRelation(
            route_relation_id=route_join[0].route_id,
            route_relation_owner=user,
        )
        new_route_relation.save()
        route_join[0].route_owner.add(new_route_relation)
        route_join.update(route_popular=route_join[0].route_popular+1)
        return HttpResponseRedirect('/route_detail/?route_id=' + str(route_join[0].route_id))
    return HttpResponseRedirect(reverse('homepage'))


@login_required
def quit_route(request):
    user = request.user if request.user.is_authenticated() else None
    if request.method == 'GET' and 'route_id' in request.GET:
        RouteRelation.objects\
            .filter(route_relation_id=request.GET.get('route_id'))\
            .filter(route_relation_owner__username__exact=user.username).delete()
        return HttpResponseRedirect('/route_detail/?route_id=' + str(request.GET.get('route_id')))


@login_required
def create_team(request):
    user = request.user if request.user.is_authenticated() else None
    if user is None:
        return HttpResponseRedirect(reverse('login'))

    state = 'unknown'
    my_routes = get_my_route(user)

    if request.method == 'POST':
        new_team = Team(
            team_name=request.POST.get('team_name', ''),
            team_creator=user,
            team_route=Route.objects.get(route_id__exact=request.POST.get('team_route', '')),
        )

        new_team.save()

        # add relation row
        new_team_relation = TeamRelation(
            team_relation_id=new_team.team_id,
            team_relation_member=user,
        )
        new_team_relation.save()
        new_team.team_member.add(new_team_relation)
        state = 'success'

    content = {
        'my_routes': my_routes,
        'state': state,
    }

    return render(request, 'travel/create_team.html', content)


def team_detail(request):
    user = request.user if request.user.is_authenticated() else None
    if request.method == 'GET' and 'team_id' in request.GET:
        team_id = request.GET.get('team_id')
        team_exact = Team.objects.get(team_id__exact=team_id)
        team_creator = User.objects.get(team_creator__team_id__exact=team_id)
        team_members = User.objects.filter(team_relation__team_relation_id__exact=team_id)
        team_route = Route.objects.get(team_route__team_id__exact=team_id)
        team_route_attractions = list()
        for i in team_route.get_route_detail():
            team_route_attractions.append(Attraction.objects.filter(attraction_id__exact=i)[0])
        updateble = (team_exact.team_creator == user)
        is_owner = (user in User.objects.filter(team_relation__team_relation_id=team_id))
        content = {
            'team': team_exact,
            'team_creator': team_creator,
            'team_members': team_members,
            'team_route': team_route,
            'team_route_attractions': team_route_attractions,
            'updateble': updateble,
            'is_owner': is_owner,
        }
        return render(request, 'travel/team_detail.html', content)
    return HttpResponseRedirect(reverse('homepage'))


def get_my_route(usr):
    my_route_relation_list = RouteRelation.objects.filter(route_relation_owner__username__exact=usr.username)
    user_own_routes_list = list()
    for ur in my_route_relation_list:
        if len(Route.objects.filter(route_id__exact=ur.route_relation_id)) > 0:
            user_own_routes_list.append(Route.objects.filter(route_id__exact=ur.route_relation_id)[0])
    my_route = get_routes(user_own_routes_list)
    return my_route


@login_required
def operate_team(request):
    user = request.user if request.user.is_authenticated() else None
    if request.method == 'GET' and request.GET.get('operate') == 'update':
        updating_team = Route.objects.filter(team_id__exact=request.GET.get('team_id'))
        if request.GET('team_name'):
            updating_team.update(team_name=request.GET.get('team_name'))

    elif request.method == 'GET' and request.GET.get('operate') == 'close':
        Team.objects.filter(team_id__exact=request.GET.get('team_id')).update(team_is_closed=True)

    else:
        team_operate = Team.objects.filter(team_id__exact=request.GET.get('team_id'))
        content = {
            'route_operate': team_operate,
            'state': 'show',
            'active_menu': 'operate_route',
        }
        return render(request, 'travel/operate_team.html', content)
    return HttpResponseRedirect(reverse('show_team'))


@login_required
def join_team(request):
    user = request.user if request.user.is_authenticated() else None
    if request.method == 'GET' and 'team_id' in request.GET:
        team_join = Team.objects.filter(team_id__exact=request.GET.get('team_id'))
        new_team_relation = TeamRelation(
            team_relation_id=team_join[0].team_id,
            team_relation_member=user,
        )
        new_team_relation.save()
        team_join[0].team_member.add(new_team_relation)
    return HttpResponseRedirect('/team_detail/?team_id=' + str(request.GET.get('team_id')))


@login_required
def quit_team(request):
    user = request.user if request.user.is_authenticated() else None
    if request.method == 'GET' and 'team_id' in request.GET:
        TeamRelation.objects\
            .filter(team_relation_id=request.GET.get('team_id'))\
            .filter(team_relation_member=user).delete()
    return HttpResponseRedirect('/team_detail/?team_id=' + str(request.GET.get('team_id')))


def show_teams(request):
    user = request.user if request.user.is_authenticated() else None

    all_teams = Team.objects.all().order_by('-team_modified_time')[:10]

    content = {'all_teams': all_teams}

    if user is not None:
        teams_create = Team.objects.filter(team_creator=user)

        teams_relation_member = TeamRelation.objects.filter(team_relation_member=user)
        teams_member = list()
        for team_relation in teams_relation_member:
            team_exact = Team.objects.filter(team_id__exact=team_relation.team_relation_id)
            if len(team_exact) > 0:
                teams_member.append(team_exact[0])

        content['teams_create'] = teams_create
        content['teams_member'] = teams_member

    return render(request, 'travel/show_teams.html', content)


def get_team_route(team_id, usr):
    team_exact = Team.objects.get(team_id__exact=team_id)
    team_creator = User.objects.get(team_creator__team_id__exact=team_id)
    team_members = User.objects.filter(team_relation__team_relation_id__exact=team_id)
    team_route = Route.objects.get(team_route__team_id__exact=team_id)
    team_route_attractions = list()
    for i in team_route.get_route_detail():
        team_route_attractions.append(Attraction.objects.filter(attraction_id__exact=i)[0])
    updateble = (team_exact.team_creator == usr)
    is_owner = (usr in User.objects.filter(team_relation__team_relation_id=team_id))
    content = {
        'team': team_exact,
        'team_creator': team_creator,
        'team_members': team_members,
        'team_route': team_route,
        'team_route_attractions': team_route_attractions,
        'updateble': updateble,
        'is_owner': is_owner,
    }
    return content


@login_required
def personal(request):
    user = request.user if request.user.is_authenticated() else None
    if user is None:
        return HttpResponseRedirect(reverse('login'))

    blog = Blog.objects.filter(blog_author=user)

    user_create_routes = Route.objects.filter(route_creator__username__exact=user.username)

    user_create_routes_list = list()

    for uor in user_create_routes:
        route_attractions = list()
        for i in uor.get_route_detail():
            route_attractions.append(Attraction.objects.filter(attraction_id__exact=i)[0])
        user_create_routes_list.append({
            'route_self': uor,
            'route_attractions': route_attractions,
        })

    user_own_routes_relations = RouteRelation.objects.filter(route_relation_owner__username__exact=user.username)

    user_own_routes_list = list()
    for ur in user_own_routes_relations:
        # user_own_routes_list.append(Route.objects.filter(route_id__exact=ur.route_relation_id)[0])
        route_own = Route.objects.filter(route_id__exact=ur.route_relation_id)[0]
        route_own_attractions = list()
        for i in route_own.get_route_detail():
            route_own_attractions.append(Attraction.objects.get(attraction_id__exact=int(i)))
        user_own_routes_list.append({
            'route_self': route_own,
            'route_attractions': route_own_attractions,
        })

    teams_create = Team.objects.filter(team_creator=user)

    teams_relation_member = TeamRelation.objects.filter(team_relation_member=user)
    teams_member = list()
    for team_relation in teams_relation_member:
        team_exact = Team.objects.filter(team_id__exact=team_relation.team_relation_id)[0]
        teams_member.append(team_exact)

    content = {
        'user': user,
        'active_menu': 'personal',
        'route_create_list': user_create_routes_list,
        'route_own': user_own_routes_list,
        'blog': blog,
        'teams_create': teams_create,
        'teams_member': teams_member,
    }

    return render(request, 'travel/personal.html', content)


def str_list_to_int(values):
    for i in range(len(values)):
        values[i] = int(values[i])
    return values
