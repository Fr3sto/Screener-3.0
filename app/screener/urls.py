from django.contrib import admin
from django.urls import path, include, register_converter
from . import views, converters
from django.conf import settings
from django.conf.urls.static import static

register_converter(converters.FloatUrlParameterConverter, 'float')

app_name = 'screener'
urlpatterns = [
    path('', views.index, name='index'),
    path('<str:symbol>-<int:tf>', views.currency_chart, name='currency_chart'),
    path('status', views.index_status, name='index_status')
]