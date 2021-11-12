from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import *
import mercadopago

def loja(request):
    data = {}
    data['item'] = produto.objects.all()
    print(data['item'])
    return render(request, 'app/loja.html', data)

@login_required
def shop_car(request):
    data = {}
    preference_data = {
        "items": [
            {
                "id": 1,
                "title": "Casaco Preto",
                "quantity": 2,
                "unit_price": 79.90
            },
            {
                "id": 2,
                "title": "Calça Jeans Azul",
                "quantity": 1,
                "unit_price": 59.90
            }
        ]
    }
    data['total_price'] = 0
    for i in preference_data['items']:
        data['total_price'] = data['total_price'] + i['quantity']*i['unit_price']

    data['total_price'] = "{:.2f}".format(data['total_price'])

    data['shop_car'] = preference_data

    try:
        sdk = mercadopago.SDK("TEST-7203257079331323-110816-df798b02b4ea47ed517f6c259ceac53b-255738925")
        preference_response = sdk.preference().create(preference_data)
        data['sdk'] = preference_response["response"]

    except:
        data['error_message'] = "Sem comunicação com a central de pagamentos!"
    return render(request, 'app/shop_car.html', data)

def shop_car_add(request):
    return redirect('/')