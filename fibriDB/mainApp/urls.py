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
    path('items/<int:pk>/', views.ItemDetail.as_view()),
    path('items/<int:pk>/highlight/', views.ItemHighlight.as_view()),
    path('users/', views.UserList.as_view()),
    path('users/<int:pk>/', views.UserDetail.as_view()),
    url('user/', views.userAccount.as_view(), name='user'),
    url('', views.mainView.as_view(), name='main'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
