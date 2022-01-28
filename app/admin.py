from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.Produto)
admin.site.register(models.ShopCar)
admin.site.register(models.Favorito)
admin.site.register(models.MercadoPagoNotification)