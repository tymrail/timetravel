from django.db import models

# Create your models here.


class Blog(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(u'标题', max_length=50)
    author = models.CharField(u'旅游景点', max_length=10)
    content = models.CharField(u'正文', max_length=2000)
    post_date = models.DateTimeField(u'发布时间', auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-post_date']
