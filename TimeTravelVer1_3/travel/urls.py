from django.conf.urls import url
from travel import views as travelviews


urlpatterns = [
    url(r'^$', travelviews.index, name='homepage'),
    url(r'^cities/$', travelviews.cities, name='cities'),
    url(r'^attractions/$', travelviews.attractions, name='attractions'),
    url(r'^attraction_info/$', travelviews.attraction_info, name='attraction_info'),
]
