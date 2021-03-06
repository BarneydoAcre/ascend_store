# Generated by Django 3.2.9 on 2022-01-30 07:36

import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='MercadoPagoNotification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_topic', models.CharField(blank=True, default='0', max_length=255)),
                ('topic', models.CharField(blank=True, default='0', max_length=255)),
                ('id_notification', models.CharField(blank=True, default='0', max_length=255)),
                ('live_mode', models.CharField(blank=True, default='0', max_length=255)),
                ('type', models.CharField(blank=True, default='0', max_length=255)),
                ('date_created', models.CharField(blank=True, default='0', max_length=255)),
                ('application_id', models.CharField(blank=True, default='0', max_length=255)),
                ('user_id', models.CharField(blank=True, default='0', max_length=255)),
                ('api_version', models.CharField(blank=True, default='0', max_length=255)),
                ('action', models.CharField(blank=True, default='0', max_length=255)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Notificação Mercado Pago',
                'verbose_name_plural': 'Notificações Mercado Pago',
                'ordering': ('created',),
            },
        ),
        migrations.CreateModel(
            name='Produto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.CharField(blank=True, max_length=255, verbose_name='Imagem')),
                ('title', models.CharField(max_length=30, verbose_name='Título')),
                ('desc', models.CharField(max_length=55, verbose_name='Descrição')),
                ('price', models.FloatField(verbose_name='Preço')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Produto',
                'verbose_name_plural': 'Produtos',
                'ordering': ('title',),
            },
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='ShopCar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7'), (8, '8'), (9, '9'), (10, '10')], verbose_name='Quantidade')),
                ('status', models.IntegerField(choices=[(1, 'carrinho'), (2, 'pedido')], default=1)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('produto', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='app.produto', verbose_name='Produto')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='app.person', verbose_name='Usuário')),
            ],
            options={
                'verbose_name': 'Carrinho de Compra',
                'verbose_name_plural': 'Carrinho de Compra',
                'ordering': ('created',),
            },
        ),
        migrations.CreateModel(
            name='Pedido',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.IntegerField(choices=[(1, 'approved'), (2, 'in_process'), (3, 'canceled')], default=2)),
                ('nome', models.CharField(max_length=255)),
                ('cpf', models.CharField(max_length=14)),
                ('cep', models.CharField(max_length=9)),
                ('estado', models.CharField(max_length=20)),
                ('cidade', models.CharField(max_length=20)),
                ('endereco', models.CharField(max_length=255)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='app.person', verbose_name='Usuário')),
            ],
            options={
                'verbose_name': 'Pedido',
                'verbose_name_plural': 'Pedidos',
                'ordering': ('created',),
            },
        ),
        migrations.CreateModel(
            name='Favorito',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('produto', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='app.produto', verbose_name='Produto')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='app.person', verbose_name='Usuário')),
            ],
            options={
                'verbose_name': 'Favorito',
                'verbose_name_plural': 'Favoritos',
                'ordering': ('created',),
            },
        ),
    ]
