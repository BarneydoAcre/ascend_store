# Generated by Django 3.2.9 on 2021-11-14 17:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_auto_20211114_0301'),
    ]

    operations = [
        migrations.CreateModel(
            name='shop_car',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_user', models.IntegerField()),
                ('id_produto', models.IntegerField()),
            ],
        ),
        migrations.DeleteModel(
            name='pedido_produtos',
        ),
    ]
