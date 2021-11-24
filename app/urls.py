from django.urls import path 
from django.contrib.auth.views import *
from . import views

app_name = 'app'

urlpatterns = [
    path('', views.loja, name='loja' ),
    path('shop-car/', views.shop_car, name='shop_car' ),
    path('shop-car/add/', views.shop_car_add, name='shop_car_add' ),
    path('shop-car/delete/', views.shop_car_delete, name='shop_car_delete' ),
    path('notifications/', views.notifications, name='notifications' ),
    path('user_account/', views.user_account, name='user_account' ),
    path("accounts/register", views.register, name="register")

    #accounts
    # path('accounts/login/', views.login, name='login' ),
    # path('accounts/login/login_auth/', views.login_auth, name='login_auth' ),
    # path('accounts/logout/', LogoutView.as_view(), name='logout'),
]