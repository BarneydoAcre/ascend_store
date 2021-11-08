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
                "title": "Casaco Preto",
                "quantity": 2,
                "unit_price": 79.90
            },
            {
                "title": "My Itens",
                "quantity": 1,
                "unit_price": 59.90
            }
        ]
    }

    preference_response = sdk.preference().create(preference_data)
    preference = preference_response["response"]
    preference['back_urls'] =  {'failure': '/', 'pending': '/', 'success': '/'}
    
    return render(request, 'app/user.html', {'sdk': preference})