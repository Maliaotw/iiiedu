from django.urls import re_path as url
from iiiedu import views

urlpatterns = [
    # url(r'^test/', views.testdb, name="testdb"),
    # url(r'^createdb/', views.createdb, name="createdb"),
    # url(r'^cleardb/', views.cleardb, name="cleardb"),

    url(r'^$', views.home_redirect),

    # chert
    url(r'^chert/course/', views.TopCourse, name="chart_course"),
    url(r'^chert/certified/', views.TopCertified, name="chart_certified"),
    url(r'^chert/lang/', views.TopLang, name="chart_lang"),
    url(r'^chert/theme/', views.TopTheme, name="chart_theme"),

    # course
    url(r'^course/$', views.course, name="course"),
    url(r'^course/cert/', views.course_cert, name="course_cert"),
    url(r'^course/full/', views.course_full, name="course_full"),
    url(r'^search/', views.search, name="search"),
    # theme
    # url(r'^series/$', views.series, name="series"),
    url(r'^theme/(?P<pk>[A-Za-z]+)', views.theme, name="theme"),

    # series
    # url(r'^series/$', views.series, name="series"),
    url(r'^series/(?P<pk>[A-Za-z]+)', views.series, name="series"),

    url(r'^testmap/', views.testmap),

    # test
    url(r'^test/page/', views.test_page, name="page"),
    url(r'^test/ajax/', views.test_ajax, name="ajax"),
]
