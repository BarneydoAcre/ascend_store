from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import mercadopago

def home(request):
    return render(request, 'app/home.html')

@login_required
def users(request):
    data = {}
    # data['users'] = User.objects.all()
    # 
    sdk = mercadopago.SDK("TEST-7203257079331323-110816-df798b02b4ea47ed517f6c259ceac53b-255738925")
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

    preference_response = sdk.preference().create(preference_data)
    data['sdk'] = preference_response["response"]

    data['shop_car'] = preference_data
    
    return render(request, 'app/user.html', data)