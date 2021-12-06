from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from .models import *
from django.contrib import messages
from store.settings.base import * 

import mercadopago
import json
import os
import requests

def loja(request):
    data = {}
    data['item'] = produto.objects.all()
    return render(request, 'app/loja.html', data)

@login_required
def shop_car_view(request):
    data = {}
    db = {}
    db['shop_car'] = shop_car.objects.filter(id_user=request.session['_auth_user_id'])
    db['produto'] = produto.objects.all()
    db['user'] = User.objects.get(id=request.session['_auth_user_id'])

    #print(request.build_absolute_uri () )



    item = ()
    for db_item in db['shop_car']:
        i = {
            "id_car_item": db_item.id,
            "id": db['produto'][db_item.id_produto-1].id,
            "title": db['produto'][db_item.id_produto-1].title,
            "quantity": 1,
            "unit_price": db['produto'][db_item.id_produto-1].price
            },
        item = item + i 

    preference_data = {
        "items": item,
        "payer": {
            "name": db['user'].username,
            "surname": db['user'].first_name,
            "email": db['user'].email,
            "phone": {
                "area_code": "11",
                "number": "4444-4444"
            },
            "identification": {
                "type": "CPF",
                "number": "19119119100"
            },
            "address": {
                "street_name": "Street",
                "street_number": 123,
                "zip_code": "06233200"
            },
            "shipments": {
                "receiver_address": {
                "street_name": "Street",
                "street_number": "123",
                "zip_code": "06233200"
            }
        },
        "back_urls": {
            "success": request.build_absolute_uri(),# + "/success/",
            "failure": request.build_absolute_uri(),# + "/failure/",
            "pending": request.build_absolute_uri(),# + "/pending/"
        },
        "auto_return": "approved",
        "payment_methods": {
            "installments": 4,
        },
        "shipments":{
            "cost": 1000,
            "mode": "not_specified",
        }
    }
    }

    data['total_price'] = 0
    for i in preference_data['items']:
        data['total_price'] = data['total_price'] + i['quantity']*i['unit_price']

    data['total_price'] = "{:.2f}".format(data['total_price'])

    data['shop_car'] = preference_data

    try:
        sdk = mercadopago.SDK(MERCADO_PAGO_ACCESS_TOKEN)
        preference_response = sdk.preference().create(preference_data)
        data['sdk'] = preference_response["response"]
    except:
        data['error_message'] = "Sem comunicação com a central de pagamentos!"
    return render(request, 'app/shop_car.html', data)

#@login_required
def notifications(request):
    topic = request.GET['topic']
    id = request.GET['id']
    response_data = {}
    response_data['result'] = 'test'
    response_data['message'] = 'Some test message'
    return HttpResponse(json.dumps(response_data), content_type="application/json", status=201)
    #return HttpResponse(status=201)

@login_required
def favoritos_view_add(request):
    try:
        data = favorito(id_user=request.POST['id-user'], id_produto=request.POST['id-item'])
        data.save()
    except:
        pass
    return redirect('/')

@login_required
def favoritos_view_delete(request):
    try:
        data = favorito.objects.filter(id_user=request.POST['id-user'], id_produto=request.POST['id-item'])
        data.delete()
    except:
        pass
    return redirect('/')

@login_required
def favoritos_view(request):
    data = {}
    data['favorito'] = favorito.objects.filter(id_user=request.session['_auth_user_id'])
    data['item'] = produto.objects.all()
    return render(request, 'app/favorito.html', data)

@login_required
def shop_car_add(request):
    try:
        data = shop_car(id_user=request.POST['id-user'], id_produto=request.POST['id-item'])
        data.save()
    except:
        pass
    return redirect('/')

@login_required
def shop_car_delete(request):
    data = shop_car.objects.filter(id_user=request.POST['id-user'], id=request.POST['id-item']).delete()
    return redirect('/shop-car/')

@login_required
def user_account(request):
    return render(request, 'app/user_account.html')