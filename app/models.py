from django.db import models
from django.contrib.auth.models import User

class Produto(models.Model):
    # image = models.FileField(upload_to='app/static/public/product_images/', blank=True)
    image = models.CharField(verbose_name="Imagem", max_length=255, blank=True)
    title = models.CharField(verbose_name="Título", max_length=30)
    desc = models.CharField(verbose_name="Descrição", max_length=55)
    price = models.FloatField(verbose_name="Preço")

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name, verbose_name_plural = "Produto", "Produtos"
        ordering = ("title",)

class pedido(models.Model):
    numero = models.IntegerField()
    usuario = models.CharField(max_length=55)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.numero
    
    class Meta:
        verbose_name, verbose_name_plural = "Pedido", "Pedidos"
        ordering = ("created",)

class ShopCar(models.Model):
    c = (
        (1,'1'),
        (2,'2'),
        (3,'3'),
        (4,'4'),
        (5,'5'),
        (6,'6'),
        (7,'7'),
        (8,'8'),
        (9,'9'),
        (10,'10'),
    )
    user = models.ForeignKey("Person", verbose_name="Usuário", on_delete=models.PROTECT)
    produto = models.ForeignKey("Produto", verbose_name="Produto", on_delete=models.PROTECT)
    quantity = models.IntegerField(verbose_name="Quantidade", choices=c)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.user)

    class Meta:
        verbose_name, verbose_name_plural = "Carrinho de Compra", "Carrinho de Compra"
        ordering = ("created",)

class Favorito(models.Model):
    user = models.ForeignKey("Person", verbose_name="Usuário", on_delete=models.PROTECT)
    produto = models.ForeignKey("Produto", verbose_name="Produto", on_delete=models.PROTECT)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.user)

    class Meta:
        verbose_name, verbose_name_plural = "Favorito", "Favoritos"
        ordering = ("created",)

class Person(User):
    class Meta:
        proxy = True

class MercadoPagoNotification(models.Model):
    id_topic = models.CharField(max_length=255)
    topic = models.CharField(max_length=255)
    json = models.CharField(max_length=255)

    class Meta:
        verbose_name, verbose_name_plural = "Notificação Mercado Pago", "Notificações Mercado Pago"
        ordering = ("id_topic",)