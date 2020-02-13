from django.conf.urls import url
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from mainApp import views

# TEMPLATE TAGGING
app_name = 'mainApp'


# URL PATTERNS
urlpatterns = [
    path('api/items/', views.ItemList.as_view(), name='api'),
    path('api/items/<int:pk>/', views.ItemDetail.as_view()),
    path('api/users/', views.UserList.as_view()),
    path('api/users/<int:pk>/', views.UserDetail.as_view()),
    url('user', views.userAccount.as_view(), name='user'),
    url('item', views.edit_item, name='item'),
    url('login', views.user_login, name='login'),
    url(r'^register/$', views.register, name='register'),
    url(r'^editprofile/$', views.edit_profile, name='editprofile'),
    url('', views.mainView.as_view(), name='main'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
