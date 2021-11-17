from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import *
import mercadopago
from django.contrib.auth import authenticate, login
import os



def logout_auth(request):
    request.session['member_id']
    return redirect('/')

def loja(request):
    data = {}
    data['item'] = produto_model.objects.all()
    return render(request, 'app/loja.html', data)

@login_required
def shop_car(request):
    data = {}
    data['shop_car_model'] = shop_car_model.objects.filter(id_user=request.session['_auth_user_id'])
    data['produto_model'] = produto_model.objects.all()

    item = ()
    for db in data['shop_car_model']:
        i = {
            "id_car_item": db.id,
            "id": data['produto_model'][db.id_produto-1].id,
            "title": data['produto_model'][db.id_produto-1].title,
            "quantity": 1,
            "unit_price": data['produto_model'][db.id_produto-1].price
            },
        item = item + i 

    preference_data = {
        "items": item
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

@login_required
def shop_car_add(request):
    try:
        data = shop_car_model(id_user=request.POST['id-user'], id_produto=request.POST['id-item'])
        data.save()
    except:
        pass
    return redirect('/')

@login_required
def shop_car_delete(request):
    data = shop_car_model.objects.filter(id_user=request.POST['id-user'], id=request.POST['id-item']).delete()
    return redirect('/shop-car/')