from django import forms
from . import models
from django.contrib.auth.models import User

class SignupForm(forms.Form):

    first_name = forms.CharField(max_length=30, label='Primeiro Nome', required=True)
    last_name = forms.CharField(max_length=30, label='Último Nome', required=True)

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget = forms.TextInput(attrs={'placeholder': 'Nome'})
        self.fields['last_name'].widget = forms.TextInput(attrs={'placeholder': 'Sobrenome'})

    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()

class AddShopCar(forms.ModelForm):
    
    class Meta:
        model = models.ShopCar

        fields = [
            'user',
            'produto',
            'quantity',
        ]

class DeleteShopCar(forms.ModelForm):

    class Meta:
        model = models.ShopCar

        fields = [
            'user',
            'produto',
        ]
        exclude = [
            'quantity',
        ]

class FavoritoForm(forms.ModelForm):

    class Meta:
        model = models.Favorito

        fields = [
            'user',
            'produto',
        ]

class PedidoForm(forms.ModelForm):

    class Meta:
        model = models.Pedido

        fields = [
            'user',
            'nome',
            'cpf',
            'cep',
            'estado',
            'cidade',
            'endereco',
        ]
        exclude = [
            'status',
        ]