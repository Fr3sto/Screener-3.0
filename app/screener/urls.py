from django.contrib import admin
from django.urls import path, include, register_converter
from . import views, converters

register_converter(converters.FloatUrlParameterConverter, 'float')

app_name = 'screener'
urlpatterns = [
    path('', views.index, name='index'),
    path('flats/<int:id>', views.current_flat, name='current_flat'),
    path('status', views.index_status, name='index_status')
]