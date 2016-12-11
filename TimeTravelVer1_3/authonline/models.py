import json
from django.db import models
from django.contrib.auth.models import User


class MyUser(models.Model):
    user = models.OneToOneField(User)
    nickname = models.CharField(max_length=16)
    permission = models.IntegerField(default=1)

    def __str__(self):
        return self.user.username


class City(models.Model):
    city_id = models.IntegerField(primary_key=True)
    city_title = models.CharField(max_length=20)
    city_name = models.CharField(max_length=40, default='')
    city_province = models.CharField(max_length=60, default='')
    city_is_rec = models.BooleanField(default=False)
    city_rec_month = models.IntegerField(default=0)
    city_intro = models.CharField(max_length=200, default='')
    city_img_src = models.CharField(max_length=100, default='')

    def __str__(self):
        return self.city_title


class Attraction(models.Model):
    attraction_id = models.IntegerField(primary_key=True)
    attraction_title = models.CharField(max_length=80)
    attraction_mapxy = models.CharField(max_length=80)
    attraction_price = models.IntegerField(default=0)
    attraction_city = models.ForeignKey(
        City,
        related_name="attraction",
    )
    attraction_is_rec = models.BooleanField(default=False)

    def __str__(self):
        return self.attraction_title


class RouteRelation(models.Model):
    route_relation_id = models.IntegerField(default=0)
    route_relation_owner = models.ForeignKey(User, related_name='route_relation')


class Route(models.Model):
    route_id = models.AutoField(primary_key=True)
    route_name = models.CharField(max_length=64, default='')
    route_detail = models.CharField(max_length=512)
    route_creator = models.ForeignKey(
        User,
        related_name='route_creator',
        default=None
    )
    route_owner = models.ManyToManyField(
        RouteRelation,
        related_name='route_owner',
    )
    route_popular = models.IntegerField(default=0)
    route_create_time = models.DateField(auto_now_add=True)
    route_modified_time = models.DateField(auto_now=True)
    route_keywords = models.CharField(max_length=40, default='')

    def __str__(self):
        return self.route_name

    def set_route_detail(self, x):
        self.route_detail = json.dumps(x)

    def get_route_detail(self):
        return json.loads(self.route_detail)



