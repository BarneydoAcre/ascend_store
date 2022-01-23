# Generated by Django 3.2.9 on 2022-01-22 20:53

import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('app', '0009_auto_20220122_1641'),
    ]

    operations = [
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
        migrations.AlterModelOptions(
            name='favorito',
            options={'ordering': ('created',), 'verbose_name': 'Favorito', 'verbose_name_plural': 'Favoritos'},
        ),
        migrations.AlterModelOptions(
            name='pedido',
            options={'ordering': ('created',), 'verbose_name': 'Pedido', 'verbose_name_plural': 'Pedidos'},
        ),
        migrations.AlterModelOptions(
            name='shop_car',
            options={'ordering': ('created',), 'verbose_name': 'Carrinho de Compra', 'verbose_name_plural': 'Carrinho de Compra'},
        ),
        migrations.AlterField(
            model_name='favorito',
            name='id_produto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='app.produto', verbose_name='Produto'),
        ),
        migrations.AlterField(
            model_name='shop_car',
            name='id_produto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='app.produto', verbose_name='Produto'),
        ),
        migrations.AlterField(
            model_name='favorito',
            name='id_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='app.person', verbose_name='Usuário'),
        ),
        migrations.AlterField(
            model_name='shop_car',
            name='id_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='app.person', verbose_name='Usuário'),
        ),
    ]
