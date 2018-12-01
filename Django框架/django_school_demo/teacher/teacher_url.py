from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [


    path(r'SmallHong/', views.do_app)
]