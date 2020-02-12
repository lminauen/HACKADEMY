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
<<<<<<< HEAD
    url('user', views.userAccount.as_view(), name='user'),
    url('login', views.user_login,name='login'),
=======
    path('users/', views.UserList.as_view()),
    path('users/<int:pk>/', views.UserDetail.as_view()),
    url('user/', views.userAccount.as_view(), name='user'),
>>>>>>> 12660fe49621d1ff2530911a6f0d19f815a8d0b4
    url('', views.mainView.as_view(), name='main'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
