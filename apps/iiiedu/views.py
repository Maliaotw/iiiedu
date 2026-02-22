import json
import os

from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseRedirect
from django.http.response import HttpResponse
from django.shortcuts import render
from django.urls import reverse
from iiiedu.models import Branch, Tag, Cate, Course, Role, UserProfile, Favorite, Reply, Menu, Series

chart_data = json.load(open(os.path.join(settings.BASE_DIR, 'static', 'data', 'iiiedu', 'chart_data.json'), 'r', encoding='utf-8'))


# chert

def TopCourse(request):
    data = chart_data['class']
    ret = {"data": data["data"], "title": data['title']}
    return render(request, "chert/index.html", ret)


def TopCertified(request):
    data = chart_data['cert']
    ret = {"data": data["data"], "title": data['title']}

    return render(request, "chert/index.html", ret)


def TopLang(request):
    data = chart_data['lang']
    ret = {"data": data["data"], "title": data['title']}

    return render(request, "chert/index.html", ret)


def TopTheme(request):
    data = chart_data['theme']
    ret = {"data": data["data"], "title": data['title']}

    return render(request, "chert/index.html", ret)


# theme

def theme(request, pk):
    data = chart_data[pk]
    ret = {"data": data["data"], "title": data['title']}

    return render(request, "theme/index.html", ret)


# series

def series(request, pk):
    s = Series.objects.get(en=pk)

    t = s.theme.all()[0]
    series = Series.objects.filter(theme=t)

    contact_list = Course.objects.filter(series=s)

    # contact_list = Course.objects.exclude(Cate__name='認證').exclude(Cate__name="養成班")
    paginator = Paginator(contact_list, 10)  # Show 10 contacts per page

    page = request.GET.get('page')
    try:
        data = paginator.page(page)
    except PageNotAnInteger:
        data = paginator.page(1)
    except EmptyPage:
        data = paginator.page(paginator.num_pages)

    page = {
        'theme': {'name': t.name, 'url': t.en},
        'series': {'name': s.name, 'url': s.en},
    }

    ret = {'data': data, 'menu': series, 'page': page}

    return render(request, "series/index.html", ret)


# Course

def course(request):
    title = '專業課程'
    contact_list = Course.objects.exclude(Tag__name__in=['認證', '養成班'])
    paginator = Paginator(contact_list, 10)  # Show 10 contacts per page

    page = request.GET.get('page')
    try:
        data = paginator.page(page)
    except PageNotAnInteger:
        data = paginator.page(1)
    except EmptyPage:
        data = paginator.page(paginator.num_pages)

    ret = {'data': data, 'title': title}

    return render(request, "course/index.html", ret)


def course_cert(request):
    q = '認證'
    contact_list = Course.objects.filter(Tag__name=q)
    paginator = Paginator(contact_list, 10)  # Show 10 contacts per page

    page = request.GET.get('page')
    try:
        data = paginator.page(page)
    except PageNotAnInteger:
        data = paginator.page(1)
    except EmptyPage:
        data = paginator.page(paginator.num_pages)

    ret = {'data': data, 'title': q}
    return render(request, "course/index.html", ret)


def course_full(request):
    q = '養成班'

    contact_list = Course.objects.filter(Tag__name=q)
    paginator = Paginator(contact_list, 10)  # Show 10 contacts per page

    page = request.GET.get('page')
    try:
        data = paginator.page(page)
    except PageNotAnInteger:
        data = paginator.page(1)
    except EmptyPage:
        data = paginator.page(paginator.num_pages)

    ret = {'data': data, 'title': q}
    return render(request, "course/index.html", ret)


# search

def search(request):
    # 支持分頁器
    data = request.GET.copy()
    if 'page' in data.keys():
        data.pop('page')
    params = {k: v for k, v in data.items() if v}

    # 拼接搜尋字段
    search_str = ""
    if params:
        for k, v in params.items():
            search_str += '&%s=%s' % (k, v)
        # print(search_str)

    name = request.GET.get('name')

    contact_list = Course.objects.filter(name__icontains=name)
    paginator = Paginator(contact_list, 10)  # Show 10 contacts per page

    page = request.GET.get('page')
    try:
        data = paginator.page(page)
    except PageNotAnInteger:
        data = paginator.page(1)
    except EmptyPage:
        data = paginator.page(paginator.num_pages)

    ret = {'data': data, 'title': "%s 搜尋結果" % name, 'search_str': search_str}

    return render(request, "search.html", ret)


def testmap(request):
    # Create two threads as follows
    return HttpResponse("ok")


def test_page(request):
    ret = {}

    return render(request, "test.html", ret)


def test_ajax(request):
    if request.POST:
        data = request.POST['data']
        # print(data)
    else:
        data = "ok"
    return HttpResponse(data)


def cleardb(request):
    Tag.objects.all().delete()
    Cate.objects.all().delete()
    Course.objects.all().delete()
    Role.objects.all().delete()
    UserProfile.objects.all().delete()
    Favorite.objects.all().delete()
    Reply.objects.all().delete()
    Menu.objects.all().delete()
    Branch.objects.all().delete()

    return HttpResponse("清理OK")


def testdb(request):
    t = Tag.objects.filter(**{'name': "tag1"})
    return HttpResponse(len(t))


# redirect
def home_redirect(request):
    return HttpResponseRedirect(
        reverse('chart_theme')
    )
