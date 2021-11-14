from django.urls import path 
from . import views

app_name = 'app'

urlpatterns = [
    path('', views.loja, name='loja' ),
    path('shop-car/<int:ku>', views.shop_car, name='shop_car' ),
    path('shop-car/add/<int:ki>/<int:ku>', views.shop_car_add, name='shop_car_add' ),
    path('shop-car/delete/<int:ki>/<int:ku>', views.shop_car_delete, name='shop_car_delete' ),
]