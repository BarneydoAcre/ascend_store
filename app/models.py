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

class Pedido(models.Model):    
    status = (
        (1,'approved'),
        (2,'in_process'),
        (3,'rejected')
    )
    user = models.ForeignKey("Person", verbose_name="Usuário", on_delete=models.PROTECT)
    price = models.FloatField(verbose_name='Valor do Pedido', null=True)
    status = models.IntegerField(choices=status, default=2, blank=False)

    nome = models.CharField(max_length=255, blank=False)
    cpf = models.CharField(max_length=14, blank=False)
    cep = models.CharField(max_length=9, blank=False)
    estado = models.CharField(max_length=20, blank=False)
    cidade = models.CharField(max_length=20, blank=False)
    endereco = models.CharField(max_length=255, blank=False)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id) + ' | ' + str(self.get_status_display())
    
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
    status = (
        (1,'carrinho'),
        (2,'pedido'),
    )
    user = models.ForeignKey("Person", verbose_name="Usuário", on_delete=models.PROTECT)
    produto = models.ForeignKey("Produto", verbose_name="Produto", on_delete=models.PROTECT)
    quantity = models.IntegerField(verbose_name="Quantidade", choices=c)
    status = models.IntegerField(choices=status, default=1)
    pedido = models.ForeignKey("Pedido", null=True, on_delete=models.CASCADE)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.produto) + ' | ' + str(self.get_status_display())

    class Meta:
        verbose_name, verbose_name_plural = "Carrinho de Compra", "Carrinho de Compra"
        ordering = ("created",)

class Favorito(models.Model):
    user = models.ForeignKey("Person", verbose_name="Usuário", on_delete=models.PROTECT)
    produto = models.ForeignKey("Produto", verbose_name="Produto", on_delete=models.PROTECT)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.user) + ' | ' + str(self.produto)

    class Meta:
        verbose_name, verbose_name_plural = "Favorito", "Favoritos"
        ordering = ("created",)

class Person(User):
    class Meta:
        proxy = True

class MercadoPagoNotification(models.Model):
    #IPN
    id_topic = models.CharField(max_length=255, default='0', blank=True)
    topic = models.CharField(max_length=255, default='0', blank=True)

    #webhook
    id_notification = models.CharField(max_length=255, default='0', blank=True)
    live_mode = models.CharField(max_length=255, default='0', blank=True)
    type = models.CharField(max_length=255, default='0', blank=True)
    date_created = models.CharField(max_length=255, default='0', blank=True)
    application_id = models.CharField(max_length=255, default='0', blank=True)
    user_id = models.CharField(max_length=255, default='0', blank=True)
    api_version = models.CharField(max_length=255, default='0', blank=True)
    action = models.CharField(max_length=255, default='0', blank=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id_notification)

    class Meta:
        verbose_name, verbose_name_plural = "Notificação Mercado Pago", "Notificações Mercado Pago"
        ordering = ("created",)