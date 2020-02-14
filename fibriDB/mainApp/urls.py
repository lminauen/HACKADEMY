from django.conf.urls import url
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from mainApp import views

# TEMPLATE TAGGING

app_name = 'mainApp'


# URL PATTERNS
urlpatterns = [
    path('api/users/', views.UserList.as_view(), name='user-list'),
    path('api/users/<int:pk>/', views.UserDetail.as_view()),
    path('api/items/', views.ItemList.as_view(), name='item-list'),
    path('api/items/<int:pk>/', views.ItemDetail.as_view()),
    path('api/', views.api_root, name='api'),
    path('editprofile', views.edit_profile, name='editprofile'),
    url(r'^api/items/nearestitems$', views.NearestItems.as_view()),
    url('user', views.userAccount.as_view(), name='user'),
    url('item', views.edit_item, name='item'),
    url('login', views.user_login, name='login'),
    path('myitems', views.myItems.as_view(), name='myitems'),
    url(r'^register/$', views.register, name='register'),
    url('', views.mainView.as_view(), name='main'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
