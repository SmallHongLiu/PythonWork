"""django_school_demo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from django.conf.urls import include

from teacher import views as tv

from teacher import teacher_url


urlpatterns = [
    path('admin/', admin.site.urls),

    # 视图函数名称只有名称，无括号和参数
    path(r'^normalmap/', tv.do_normalmap),



    # 尖号表示以后面内容开头的表达式
    # 圆括号表示的是一个参数，里面的内容作为参数传递给被调用的函数
    # 参数名称以问好加大写P开头，尖括号里面就是参数的名字
    # 尖括号后表示正则，【0-9】表示内容仅能是有0-9的数字构成
    # 后面大括号表示出现的次数，此处4表示只能出现四个0-9的数字
    path(r'^withparam/(?P<year>[0-9]{4}/(?P<month>[0, 1][0-9])', tv.withparam), # 正常映射

    # 比如约定，凡是由teacher模块处理的视图的url都以teacher开头
    path(r'^teacher/', include(teacher_url)),

    path(r'^book/(?:page-(?P<pn>\d+)/)$', tv.do_param2),

    path(r'^yourname/$', tv.extra_name, {'name': 'SmallHong'}),

    # 反向解析
    path('r^yourname/$', tv.revParse, name='askname'),

]
