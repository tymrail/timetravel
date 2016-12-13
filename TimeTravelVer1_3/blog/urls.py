from django.conf.urls import url
from blog import views as blogviews


urlpatterns = [
    url(r'^create_blog/$', blogviews.create_blog, name='create_blog'),
    url(r'^view_all_blog/$', blogviews.view_all_blog, name='view_all_blog'),
    url(r'^blog_detail/$', blogviews.blog_detail, name='blog_detail'),
    url(r'^like_blog/$', blogviews.like_blog, name='like_blog'),
    url(r'^delete_blog/$', blogviews.delete_blog, name='delete_blog'),
    url(r'^update_blog/$', blogviews.update_blog, name='update_blog'),
]
