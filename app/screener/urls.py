from django.contrib import admin
from django.urls import path, include, register_converter
from . import views, converters

register_converter(converters.FloatUrlParameterConverter, 'float')

app_name = 'screener'
urlpatterns = [
    path('', views.index, name='index'),
    path('positions', views.positions, name='positions'),
    path('positions/<str:id>', views.current_deal, name='current_deal'),
    path('status_check', views.status_check, name='status_check'),
    path('close_level/<str:symbol>/<float:level>', views.chart_close_level, name='chart_close_level'),
    path('position/<str:symbol>', views.current_position, name='current_position'),
]