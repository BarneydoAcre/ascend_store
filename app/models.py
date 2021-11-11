from django.db import models

class produto(models.Model):
    nome = models.CharField(max_length=30)