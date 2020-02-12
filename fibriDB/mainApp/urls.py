from django.conf.urls import url
from django.conf.urls import include
from django.urls import path
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns

from mainApp import views

from mainApp import views

# TEMPLATE TAGGING
app_name = 'mainApp'


# URL PATTERNS
urlpatterns = [
    path('items/', views.ItemList.as_view()),
    path('items/<int:pk>', views.ItemDetail.as_view()),
    url('user', views.userAccount.as_view(), name='user'),
    url('login', views.user_login,name='login'),
    url('', views.mainView.as_view(), name='main'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
