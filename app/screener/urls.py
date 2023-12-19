from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'screener'
urlpatterns = [
    path('', views.index, name='index'),
    path('<str:symbol>/order_book', views.order_book_chart, name='order_book_chart'),
    path('<str:symbol>-<int:tf>', views.currency_chart, name='currency_chart'),
    path('big_orders', views.big_orders, name='big_orders'),
    path('positions', views.positions, name='positions'),
]