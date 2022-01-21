from django.urls import path 
from . import views 

app_name = 'app_admin'

urlpatterns = [
    path('app_admin/', views.produtos),
]