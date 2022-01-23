from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages

from .forms import *
from .models import *
from django.contrib import messages
from store.settings.base import * 

import mercadopago
import json
import os
import requests

def loja(request):
    data = {}
    data['item'] = Produto.objects.all()
    data['form'] = AddShopCar

    return render(request, 'app/loja.html', data)

@login_required
def shop_car_view(request):
    db = {}

    db['form'] = DeleteShopCar

    db['shop_car'] = ShopCar.objects.filter(user=request.session['_auth_user_id'])
    prod = Produto.objects.all()
        
    db['total_price'] = 0
    for i in db['shop_car']:
        for p in prod:
            if i.produto.id == p.id:
                db['total_price'] = db['total_price'] + i.quantity*p.price

    return render(request, 'app/shop_car.html', db)
    

@login_required
def shop_car_add(request):
    if request.method == "POST":
        form = AddShopCar(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.INFO, "Adicionado ao Carrinho!")
            return redirect('/')
        else:
            messages.add_message(request, messages.INFO, "Falha ao Adicionar ao Carrinho! Formulário inválido!")
            return redirect('/')
    else:
        messages.add_message(request, messages.INFO, "Falha ao Adicionar ao Carrinho!")
        return redirect('/')

@login_required
def shop_car_delete(request):
    if request.method == "POST":
        form = DeleteShopCar(request.POST or None)
        if form.is_valid():
            messages.add_message(request, messages.INFO, "Produto Removido do Carrinho!")
            ShopCar.objects.filter(id=request.POST['id_item'], user=request.POST['user'], produto=request.POST['produto']).delete()
            return redirect('/shop-car/')
        else:
            messages.add_message(request, messages.INFO, "Falha ao Remover do Carrinho! Formulário Inválido!")
            return redirect('/shop-car/', form)
    else:   
        messages.add_message(request, messages.INFO, "Falha ao Remover do Carrinho!")
        return redirect('/shop-car/')


#@login_required
def buy_process(request):
    data = {}
    db = {}
    prod = Produto.objects.all()
    db['user'] = User.objects.get(id=request.session['_auth_user_id'])

    return_url = request.build_absolute_uri ()  #pegar a url base, independente do host



    item = ()
    for db_item in db['shop_car']:
        i = {
            "id_car_item": db_item.id,
            "id": prod[db_item.produto.id-1].title,             #aqui o -1 signfica a posição no array
            "title": prod[db_item.produto.id-1].title,
            "quantity": db_item['quantity'],
            "unit_price": prod[db_item.produto_id-1].price
            },
        item = item + i 

    preference_data = {
        "items": item,
        "notification_url": 'https://ascend-store.herokuapp.com/notifications/',
        "payer": {
            "name": db['user'].username,
            "surname": db['user'].first_name,
            "email": db['user'].email,
            "phone": {
                "area_code": "55",
                "number": "98529-8743"
            },
            "identification": {
                "type": "CPF",
                "number": "08307014190"
            },
            "address": {
                "street_name": "Insurgentes Sur",
                "street_number": 1602,
                "zip_code": "78134-190"
            },
        },
        "back_urls": {
            "success": return_url,# + "/success/",
            "failure": return_url,# + "/failure/",
            "pending": return_url,# + "/pending/"
        },
        "auto_return": "approved",
        "payment_methods": {
            "excluded_payment_methods": [
                {
                    "id": "amex"
                }
            ],
            "excluded_payment_types": [
                {
                    "id": "ticket"
                }
            ],
            "installments": 6
        },
    }

    data['shop_car'] = preference_data

    try:
        sdk = mercadopago.SDK(MERCADO_PAGO_ACCESS_TOKEN)
        preference_response = sdk.preference().create(preference_data)
        data['sdk'] = preference_response["response"]
    except:
        data['error_message'] = "Sem comunicação com a central de pagamentos!"
    return render(request, 'app/shop_car.html', data)


@csrf_exempt
def notifications(request):
    response_data = {}
    if request.method == "POST":
        data = json.loads(request.body)
        print(request.body)
        return HttpResponse(json.dumps(response_data), content_type="application/json", status=201)
    else:
        return HttpResponse(status=400)

@login_required
def favoritos_view_add(request):
    try:
        data = favorito.objects.filter(id_user=request.POST['id-user'], id_produto=request.POST['id-item'])
        if data:
            pass
        else:
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
    return redirect('/favoritos/')

@login_required
def favoritos_view(request):
    data = {}
    data['favorito'] = favorito.objects.filter(id_user=request.session['_auth_user_id'])
    data['item'] = Produto.objects.all()
    return render(request, 'app/favorito.html', data)


@login_required
def user_account(request):
    return render(request, 'app/user_account.html')