from django.conf.urls import url
from django.urls import path
from mainApp import views

# TEMPLATE TAGGING
app_name = 'mainApp'

# URL PATTERNS
urlpatterns = [
    url('', views.mainView.as_view(), name='main'),
]
