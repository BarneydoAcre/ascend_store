# Generated by Django 3.2.9 on 2021-11-18 16:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0017_auto_20211118_1222'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='produto_model',
            name='created',
        ),
        migrations.RemoveField(
            model_name='produto_model',
            name='updated',
        ),
    ]