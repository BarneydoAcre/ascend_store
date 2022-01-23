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

class FavoritoForm(forms.ModelForm):

    class Meta:
        model = Favorito

        fields = [
            
            'user',
            'produto',
        ]
        
        exclude =['quantity',]