from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'screener'
urlpatterns = [
    path('', views.index, name='index'),
    path('<str:symbol>/order_book', views.order_book_chart, name='order_book_chart'),
    path('<str:symbol>-<int:tf>', views.currency_chart, name='currency_chart'),
    path('big_orders', views.big_orders, name='big_orders'),
    path('level/<int:id>', views.current_level, name='current_level'),
    path('positions', views.positions, name='positions'),
    path('positions/<str:id>', views.current_deal, name='current_deal'),
    path('status_check', views.status_check, name='status_check'),
    path('close_levels', views.chart_close_levels, name='chart_close_levels'),
    path('close_level/<str:symbol>', views.chart_close_level, name='chart_close_level'),
]