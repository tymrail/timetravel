from django.conf.urls import url
from authonline import views as authviews


urlpatterns = [
    # url(r'^$', authviews.index, name='homepage'),
    url(r'^signup/$', authviews.signup, name='signup'),
    url(r'^login/$', authviews.login, name='login'),
    url(r'^logout/$', authviews.logout, name='logout'),
    url(r'^set_password/$', authviews.set_password, name='set_password'),
]
