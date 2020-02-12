from django.conf.urls import url
from django.conf.urls import include
from django.urls import path
from rest_framework import routers
from mainApp import views

from mainApp import views

# TEMPLATE TAGGING
app_name = 'mainApp'


# URL PATTERNS
urlpatterns = [
    path('/items', views.item_list),
    path('/items/<int:pk>', views.item_detail),
    url('/user', views.userAccount.as_view(), name='user'),
    url('', views.mainView.as_view(), name='main'),
]
