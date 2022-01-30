from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.utils.datastructures import MultiValueDictKeyError

from . import forms
from . import models
from django.contrib import messages
from store.settings.base import * 

import mercadopago
import json
import os
import requests

def loja(request):
    data = {}
    try:
        data['item'] = models.Produto.objects.filter(title=request.GET['title'])
    except MultiValueDictKeyError:
        data['item'] = models.Produto.objects.all()
        
    data['form_shop_car'] = forms.AddShopCar

    return render(request, 'app/loja.html', data)

@login_required
def shop_car(request):
    db = {}
    db['form'] = forms.PedidoForm
    db['shop_car'] = models.ShopCar.objects.filter(user=request.session['_auth_user_id'], status=1)
    user = User.objects.get(id=request.session['_auth_user_id'])

    db['total_price'] = 0
    item = ()
        
    for num,i in enumerate(db['shop_car'],start=1):
        db['total_price'] = db['total_price'] + i.quantity*i.produto.price

        i = {
            "id": i.produto.id,
            "title": i.produto.title,
            "quantity": i.quantity,
            "unit_price": i.produto.price
        },
        item = item + i 

    return_url = request.build_absolute_uri ()  #pegar a url base, independente do host



    preference_data = {
        "items": item,
        "notification_url": 'https://ascend-store.herokuapp.com/notifications/',
        "external_reference": "Reference_1234",
        "payer": {
            "name": user.username,
            "surname": user.first_name,
            "email": user.email,
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
            "success": "127.0.0.1:8000/notifications/",# + "/success/",
            "failure": "127.0.0.1:8000/notifications/",# + "/failure/",
            "pending": "127.0.0.1:8000/notifications/",# + "/pending/"
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

    try:
        sdk = mercadopago.SDK(MERCADO_PAGO_ACCESS_TOKEN)
        preference_response = sdk.preference().create(preference_data)
        db['sdk'] = preference_response["response"]
    except:
        messages.add_message(request,messages.INFO,"Sem comunicação com a central de pagamentos!")

    return render(request, 'app/shop_car.html', db)
    

@login_required
def shop_car_add(request):
    if request.method == "POST":
        form = forms.AddShopCar(request.POST)
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
        form = forms.DeleteShopCar(request.POST or None)
        if form.is_valid():
            messages.add_message(request, messages.INFO, "Produto Removido do Carrinho!")
            models.ShopCar.objects.filter(id=request.POST['id_item'], user=request.POST['user'], produto=request.POST['produto']).delete()
            return redirect('/shop-car/')
        else:
            messages.add_message(request, messages.INFO, "Falha ao Remover do Carrinho! Formulário Inválido!")
            return redirect('/shop-car/', form)
    else:   
        messages.add_message(request, messages.INFO, "Falha ao Remover do Carrinho!")
        return redirect('/shop-car/')

@csrf_exempt
def notifications(request):
    response_data = {}
    try: 
        if request.GET['topic']:
            return HttpResponse(status=201)
    except:
        pass

    try:
        if request.GET['status']:
            get = {}
            get['collection_id'] = request.GET['collection_id']
            get['status'] = request.GET['status']
            get['external_reference'] = request.GET['external_reference'].replace('null','Nenhum')
            get['merchant_order_id'] = request.GET['merchant_order_id']
            get['payment_type'] = request.GET['payment_type'].replace('credit_card','Cartão de Crédito')
            get['preference_id'] = request.GET['preference_id']
            get['site_id'] = request.GET['site_id']
            get['processing_mode'] = request.GET['processing_mode']
            get['merchant_account_id'] = request.GET['merchant_account_id']

            return render(request, "app/notification.html", get)

    except MultiValueDictKeyError:
        pass

    try:   
        if request.method == "POST":
            body = json.loads(request.body.decode('UTF-8'))
            models.MercadoPagoNotification(
                id_topic=request.GET['id'],
                topic=request.GET['topic'],
                id_notification=body['id'],
                live_mode=body['live_mode'],
                type=body['type'],
                date_created=body['date_created'],
                application_id=body['application_id'],
                user_id=body['user_id'],
                api_version=body['api_version'],
                action=body['action'],
            ).save()
        return HttpResponse(json.dumps(response_data), content_type="application/json", status=201)
    except MultiValueDictKeyError:
        pass

    return HttpResponse(status=201)


@login_required
def favoritos(request):
    data = {}
    data['favorito'] = models.Favorito.objects.filter(user=request.session['_auth_user_id'])
    data['form_shop_car'] = forms.AddShopCar
    return render(request, 'app/favorito.html', data)

@login_required
def favoritos_add(request):
    if request.method == "POST":
        form = forms.FavoritoForm(request.POST)
        if form.is_valid():
            valid = models.Favorito.objects.filter(user=request.POST['user'], produto=request.POST['produto'])
            if valid:
                messages.add_message(request, messages.INFO, "Esse produto já está nos favoritos!")
            else: 
                form.save()
                messages.add_message(request, messages.INFO, "Produto adicionado aos Favoritos!")
        else:
            messages.add_message(request, messages.INFO, "Falha ao adicionar aos Favoritos! Formulário Inválido!")
    else:
        messages.add_message(request, messages.INFO, "Falha ao adicionar aos Favoritos!")
    return redirect('/')

@login_required
def favoritos_delete(request):
    if request.method == "POST":
        form = forms.FavoritoForm(request.POST)
        if form.is_valid():
            models.Favorito.objects.filter(id=request.POST['id_favorito'], user=request.POST['user'], produto=request.POST['produto']).delete()
            messages.add_message(request, messages.INFO, "Produto removido dos Favoritos!")
        else:
            messages.add_message(request, messages.INFO, "Falha ao remover dos Favoritos! Formulário Inválido!")
    else:
        messages.add_message(request, messages.INFO, "Falha ao remover dos Favoritos!")
    return redirect('/favoritos/')

@login_required
def pedidos(request):
    data = {}
    data['pedidos'] = models.Pedido.objects.filter(user=request.session['_auth_user_id'])
    return render(request, 'app/pedidos.html', data)

@login_required
def pedidos_add(request):
    if request.method == "POST":
        form = forms.PedidoForm(request.POST)
        if form.is_valid():
            form.save()
            data = models.ShopCar.objects.filter(user=request.session['_auth_user_id'])
            for d in data:
                d.status = 2
                d.save()
            messages.add_message(request, messages.INFO, "Pedido gerado com sucesso!")
        else:
            print('teste')
            messages.add_message(request, messages.INFO, "Falha ao gerar pedido! Erro de formulário")
    else: 
        messages.add_message(request, messages.INFO, "Falha ao gerar pedido!")
    return redirect('/pedidos/')

@login_required
def pedidos_delete(request):

    return redirect('/pedidos/')

@login_required
def user_account(request):
    return render(request, 'app/user_account.html')