from django.urls import path 
from django.views.decorators.csrf import csrf_exempt
from . import views

app_name = 'app'

urlpatterns = [
    path('', views.loja, name='loja' ),
    path('shop-car/', views.shop_car, name='shop_car' ),
    path('shop-car/add/', views.shop_car_add, name='shop_car_add' ),
    path('shop-car/delete/', views.shop_car_delete, name='shop_car_delete' ),
    path('favoritos/', views.favoritos, name='favorito'),
    path('favoritos/add/', views.favoritos_add, name='favoritos_add'),
    path('favoritos/delete/', views.favoritos_delete, name='favoritos_delete'),
    path('pedidos/', views.pedidos, name='pedidos'),
    path('pedidos/add/', views.pedidos_add, name='pedidos_add'),
    path('pedidos/delete/', views.pedidos_delete, name='pedidos_delete'),
    path('notifications/', csrf_exempt(views.notifications), name='notifications' ),
    path('user_account/', views.user_account, name='user_account' ),
    

    #accounts
    # path('accounts/login/', views.login, name='login' ),
    # path('accounts/login/login_auth/', views.login_auth, name='login_auth' ),
    # path('accounts/logout/', LogoutView.as_view(), name='logout'),
]