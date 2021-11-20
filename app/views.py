from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from .models import *
from store.settings.base import * 


import mercadopago
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
    db = {}
    db['shop_car_model'] = shop_car_model.objects.filter(id_user=request.session['_auth_user_id'])
    db['produto_model'] = produto_model.objects.all()
    db['user_model'] = User.objects.get(id=request.session['_auth_user_id'])

    print(request.build_absolute_uri () )



    item = ()
    for db_item in db['shop_car_model']:
        i = {
            "id_car_item": db_item.id,
            "id": db['produto_model'][db_item.id_produto-1].id,
            "title": db['produto_model'][db_item.id_produto-1].title,
            "quantity": 1,
            "unit_price": db['produto_model'][db_item.id_produto-1].price
            },
        item = item + i 

    preference_data = {
        "items": item,
        "payer": {
            "name": db['user_model'].username,
            "surname": db['user_model'].first_name,
            "email": db['user_model'].email,
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

@login_required
def notifications(request):
    topic = request.GET['topic']
    id = request.GET['id']
    print(topic,id)
    return render(request, 'mercado_pago/notification.html')

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