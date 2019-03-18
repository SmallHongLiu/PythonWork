from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse

from django.core.urlresolvers import reverse

# 视图函数，需要一个参数，类型应该是HttpRequest
def do_normalmap(request):
    return HttpResponse('This is normal map')

def withparam(request, year, month):
    return HttpResponse('This is with param {0}, {1}'.format(year, month))

def do_app(request):
    return HttpResponse('这是个子路由')

def do_param2(request, pn):
    return HttpResponse('Page number is {0}'.format(pn))

def extra_param(request, name):
    return HttpResponse('My name is {0}'.format(name))

def revParse(request):
    return HttpResponse('Your requested URL is {0}'.format(reverse.askname))

