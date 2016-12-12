from django.contrib import admin
from authonline.models import City, Attraction, Route, MyUser, RouteRelation, Team, TeamRelation

admin.site.register(City)
admin.site.register(Attraction)
admin.site.register(Route)
admin.site.register(MyUser)
admin.site.register(RouteRelation)
admin.site.register(Team)
admin.site.register(TeamRelation)
