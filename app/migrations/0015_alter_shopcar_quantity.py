# Generated by Django 3.2.9 on 2022-01-22 22:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0014_alter_shopcar_quantity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shopcar',
            name='quantity',
            field=models.IntegerField(verbose_name='Quantidade'),
        ),
    ]
