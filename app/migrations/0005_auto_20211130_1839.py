# Generated by Django 3.2.9 on 2021-11-30 22:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_alter_produto_model_file'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='pedido_model',
            new_name='pedido',
        ),
        migrations.RenameModel(
            old_name='produto_model',
            new_name='produto',
        ),
        migrations.RenameModel(
            old_name='shop_car_model',
            new_name='shop_car',
        ),
    ]
