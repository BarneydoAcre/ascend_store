from django import forms
from .models import *

class AddShopCar(forms.ModelForm):
    
    class Meta:
        model = ShopCar

        fields = [
            'user',
            'produto',
            'quantity',
        ]

class DeleteShopCar(forms.ModelForm):

    class Meta:
        model = ShopCar

        fields = [
            'user',
            'produto',
        ]
        exclude =['quantity',]