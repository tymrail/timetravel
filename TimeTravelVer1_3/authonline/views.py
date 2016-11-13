from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth.models import User
from django.contrib import auth
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from authonline.models import MyUser
from django.core.urlresolvers import reverse
from authonline.utils import permission_check
import re


def index(request):
    user = request.user if request.user.is_authenticated() else None
    content = {
        'active_menu': 'homepage',
        'user': user,
    }
    return render(request, 'authonline/index.html', content)


def signup(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('homepage'))
    state = None
    if request.method == 'POST':
        password = request.POST.get('password', '')
        password_repeat = request.POST.get('password_repeat', '')
        username = request.POST.get('username', '')
        email = request.POST.get('email', '')
        if password == '' or password_repeat == '':
            state = 'password_empty'
        elif username == '':
            state = 'username_empty'
        elif email == '':
            state = 'email_empty'
        elif password != password_repeat:
            state = 'repeat_error'
        else:
            if User.objects.filter(username=username):
                state = 'user_exist'
            elif User.objects.filter(email=email):
                state = 'email_exist'
            else:
                new_user = User.objects.create_user(username=username,
                                                    password=password,
                                                    email=email)
                new_user.save()
                new_my_user = MyUser(user=new_user,
                                     nickname=request.POST.get('nickname', username))
                new_my_user.save()
                state = 'success'

    content = {
        'active_menu': 'homepage',
        'state': state,
        'user': None,
    }
    return render(request, 'authonline/signup.html', content)


def login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('homepage'))
    state = None
    if request.method == 'POST':
        userlogin = request.POST.get('userlogin', '')
        password = request.POST.get('password', '')
        email_re = r'(^[\w-]+(\.[\w-]+)*@[\w-]+(\.[\w-]+)+$)'
        if re.match(email_re, userlogin):
            user = auth.authenticate(email=userlogin, password=password)
        else:
            user = auth.authenticate(username=userlogin, password=password)

        if user is not None:
            auth.login(request, user)
            return HttpResponseRedirect(reverse('homepage'))
        else:
            state = 'not_exist_or_pwd_error'

    content = {
        'active_menu': 'homepage',
        'state': state,
        'user': None,
    }

    return render(request, 'authonline/login.html', content)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('homepage'))


@login_required
def set_password(request):
    user = request.user
    state = None
    if request.method == 'POST':
        old_password = request.POST.get('old_password', '')
        new_password = request.POST.get('new_password', '')
        repeat_password = request.POST.get('repeat_password', '')
        if user.check_password(old_password):
            if not new_password:
                state = 'empty_new_password'
            elif new_password != repeat_password:
                state = 'repeat_error'
            else:
                user.set_password(new_password)
                user.save()
                state = 'success'
        else:
            state = 'password_error'

    content = {
        'user': user,
        'active_menu': 'homepage',
        'state': state,
    }

    return render(request, 'authonline/set_password.html', content)

