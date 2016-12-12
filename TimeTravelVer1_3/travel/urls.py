from django.conf.urls import url
from travel import views as travelviews


urlpatterns = [
    url(r'^$', travelviews.index, name='homepage'),
    url(r'^personal/$', travelviews.personal, name='personal'),
    url(r'^cities/$', travelviews.cities, name='cities'),
    url(r'^attractions/$', travelviews.attractions, name='attractions'),
    url(r'^attraction_info/$', travelviews.attraction_info, name='attraction_info'),
    url(r'^create_route/$', travelviews.create_route, name='create_route'),
    url(r'^route_detail/$', travelviews.route_detail, name='route_detail'),
    url(r'^show_routes/$', travelviews.show_routes, name='show_routes'),
    url(r'^join_route/$', travelviews.join_route, name='join_route'),
    url(r'^quit_route/$', travelviews.quit_route, name='quit_route'),
    url(r'^create_team/$', travelviews.create_team, name='create_team'),
    url(r'^team_detail/$', travelviews.team_detail, name='team_detail'),
    url(r'^quit_team/$', travelviews.quit_team, name='quit_team'),
    url(r'^join_team/$', travelviews.join_team, name='join_team'),
    url(r'^show_teams/$', travelviews.show_teams, name='show_teams'),
]
