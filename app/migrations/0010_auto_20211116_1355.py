# Generated by Django 3.2.9 on 2021-11-16 17:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_remove_shop_car_model_quantity'),
    ]

    operations = [
        migrations.DeleteModel(
            name='UploadFile_model',
        ),
        migrations.AddField(
            model_name='produto_model',
            name='file',
            field=models.FileField(default=1, upload_to=''),
            preserve_default=False,
        ),
    ]