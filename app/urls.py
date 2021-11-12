from django.urls import path 
from . import views

app_name = 'app'

urlpatterns = [
    path('', views.loja, name='loja' ),
    path('shop_car/', views.shop_car, name='shop_car' ),
    path('shop-car/add/', views.shop_car_add, name='shop_car_add' ),
]