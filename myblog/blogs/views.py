from django.http import HttpResponseRedirect
from django.shortcuts import render
from blogs.models import Blog


def blog_form(request):
    state = None
    if request.method == 'POST':
        if Blog.objects.all().exists():
            blog_last = Blog.objects.all().order_by('-id')[0]
            Blog.id = int(blog_last.id) + 1
        else:
            Blog.id = 0
        new_blog = Blog(
            id=Blog.id,
            title=request.POST.get('title', ''),
            author=request.POST.get('author', ''),
            content=request.POST.get('content', ''),
        )
        new_blog.save()
        state = 'success'
    con = {
        'state': state,
    }
    return render(request, 'yemian/blog_form.html', con)


def blog_del(request):
    blog_list = Blog.objects.all()
    if request.GET.get('operate') == 'delete':
        bid_ = request.GET['id']
        Blog.objects.filter(id=bid_).delete()
    content = {
        'blog_list': blog_list,
    }

    return render(request, 'yemian/blog_list.html', content)


def blog_view(request):
    errors = []
    if 'id' in request.GET:
        bid_ = request.GET['id']
        blog = Blog.objects.get(id=bid_)
        return render(request, 'yemian/blog_view.html',{'blog':blog})
    else:
        errors.append("参数异常错误")
        return render(request, 'yemian/blog_list.html',{'errors':errors})


def blog_edit(request):
    content = dict()
    if request.method == 'POST':
        bid_ = request.POST.get('id')
        blog = Blog.objects.filter(id__iexact=bid_)

        if request.POST.get('new_title'):
            blog.update(title=request.POST.get('new_title'))
        if request.POST.get('new_author'):
            blog.update(author=request.POST.get('new_author'))
        if request.POST.get('new_content'):
            blog.update(content=request.POST.get('new_content'))
        blog_info = Blog.objects.get(id=bid_)
        content = {
            'blog': blog_info,
        }
    elif request.method == 'GET':
        bid_ = request.GET.get('id')
        blog = Blog.objects.get(id=bid_)
        content = {
            'blog': blog,
        }

    return render(request, 'yemian/blog_edit.html', content)
