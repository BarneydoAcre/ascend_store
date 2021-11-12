from django.db import models

class produto(models.Model):
    title = models.CharField(max_length=30)
    desc = models.CharField(max_length=55)
    price = models.FloatField()

    def __str__(self):
        return self.title