# Generated by Django 3.2.9 on 2022-01-30 18:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='shopcar',
            name='pedido',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='app.pedido'),
        ),
    ]