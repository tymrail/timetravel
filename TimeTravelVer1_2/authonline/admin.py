from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from authonline.models import *


class MyUserInLine(admin.StackedInline):
    model = MyUser
    can_delete = False


class UserAdmin(BaseUserAdmin):
    inlines = (MyUserInLine,)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)

