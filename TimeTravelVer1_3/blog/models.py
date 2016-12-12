from django.db import models
from django.contrib.auth.models import User
from authonline.models import MyUser, City, Attraction, Team, TeamRelation, Route, RouteRelation


class Blog(models.Model):
    blog_id = models.AutoField(primary_key=True)
    blog_title = models.CharField(max_length=64, default='')
    blog_text = models.TextField()
    blog_author = models.ForeignKey(
        User,
        related_name='user_blog',
    )
    blog_city = models.ForeignKey(
        City,
        related_name='city_blog',
    )
    blog_popular = models.IntegerField(default=0)
    blog_post_date = models.DateTimeField(auto_now_add=True)
    blog_modified_date = models.DateTimeField(auto_now=True)
    blog_intro = models.CharField(max_length=64, default='')

    def __str__(self):
        return self.blog_title

    class Meta:
        ordering = ['-blog_modified_date']
