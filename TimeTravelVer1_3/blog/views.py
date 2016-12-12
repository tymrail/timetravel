from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt

from authonline.models import MyUser, City, Attraction, Team, TeamRelation, Route, RouteRelation

from django.contrib.auth.decorators import user_passes_test, login_required

from blog.models import Blog


@login_required
def create_blog(request):
    user = request.user if request.user.is_authenticated() else None
    if user is None:
        return HttpResponseRedirect(reverse('login'))
    if request.method == 'POST':
        new_blog = Blog(
            blog_title=request.POST.get('blog_title', ''),
            blog_text=request.POST.get('blog_text', ''),
            blog_intro=request.POST.get('blog_intro', ''),
            blog_author=user,
            blog_city=City.objects.get(city_id=request.POST.get('blog_city_id')),
        )
        new_blog.save()
    cities = City.objects.all()
    content = {
        'user': user,
        'active_menu': 'create_blog',
        'city': cities,
    }
    return render(request, 'blog/create_blog.html', content)


def view_all_blog(request):
    user = request.user if request.user.is_authenticated() else None

    blog = Blog.objects.all()

    content = {
        'user': user,
        'blog': blog,
    }

    return render(request, 'blog/view_all_blog.html', content)


def blog_detail(request):
    user = request.user if request.user.is_authenticated() else None

    if request.method == 'GET' and 'blog_id' in request.GET:
        blog_exact = Blog.objects.get(blog_id=request.GET.get('blog_id'))
        update_permission = (user == blog_exact.blog_author)
        content = {
            'user': user,
            'blog_exact': blog_exact,
            'update_permission': update_permission,
        }

        return render(request, 'blog/blog_detail.html', content)


def update_blog(request):
    user = request.user if request.user.is_authenticated() else None

    if request.method == 'POST' and 'blog_id' in request.POST:
        blog = Blog.objects.filter(blog_id__exact=request.POST.get('blog_id'))

        if 'blog_title' in request.POST:
            blog.update(blog_title=request.POST.get('blog_title'))
        if 'blog_text' in request.POST:
            blog.update(blog_text=request.POST.get('blog_text'))
        if 'blog_intro' in request.POST:
            blog.update(blog_intro=request.POST.get('blog_intro'))
        if 'blog_city_id' in request.POST:
            blog.update(blog_city=City.objects.get(city_id=request.POST.get('blog_city_id')))

        return HttpResponseRedirect('/blog_detail/?blog_id=' + str(blog[0].blog_id))

    elif request.method == 'GET' and 'blog_id' in request.GET:
        blog = Blog.objects.filter(blog_id__exact=request.GET.get('blog_id'))[0]
        city = City.objects.all()
        content = {
            'user': user,
            'blog': blog,
            'city': city,
        }

        return render(request, 'blog/update_blog.html', content)

    else:
        return HttpResponseRedirect(reverse('view_all_blog'))


@login_required
def like_blog(request):
    user = request.user if request.user.is_authenticated() else None

    if request.method == 'GET' and 'blog_id' in request.GET:
        blog = Blog.objects.filter(blog_id__exact=request.GET.get('blog_id'))

        blog.update(blog_popular=blog[0].blog_popular + 1)
        return HttpResponseRedirect('/blog_detail/?blog_id=' + str(blog[0].blog_id))

    else:
        return HttpResponseRedirect(reverse('view_all_blog'))


@login_required
def delete_blog(request):
    user = request.user if request.user.is_authenticated() else None

    if request.method == 'GET' and request.GET.get('operate') == 'delete' and 'blog_id' in request.GET:
        Blog.objects.filter(blog_id__exact=request.GET.get('blog_id')).delete()
        return HttpResponseRedirect(reverse('view_all_blog'))

    else:
        return render(request, 'authonline/404.html')












