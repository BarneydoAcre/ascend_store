from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages

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
    data['item'] = models.Produto.objects.filter(title=request.GET['title']) if request.GET else models.Produto.objects.all()
        
    data['form_shop_car'] = forms.AddShopCar

    return render(request, 'app/loja.html', data)

@login_required
def shop_car_view(request):
    db = {}
    db['form'] = forms.DeleteShopCar
    db['shop_car'] = models.ShopCar.objects.filter(user=request.session['_auth_user_id'])
    user = User.objects.get(id=request.session['_auth_user_id'])

    db['total_price'] = 0
    item = ()
    for i in db['shop_car']:
        db['total_price'] = db['total_price'] + i.quantity*i.produto.price

        i = {
            "id": i.produto.id,             #aqui o -1 signfica a posição no array
            "title": i.produto.title,
            "quantity": i.quantity,
            "unit_price": i.produto.price
        },
        item = item + i 

    return_url = request.build_absolute_uri ()  #pegar a url base, independente do host



    preference_data = {
        "items": item,
        "notification_url": 'https://ascend-store.herokuapp.com/notifications/',
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
            "success": "https://ascend-store.herokuapp.com/?msg=success",# + "/success/",
            "failure": "https://ascend-store.herokuapp.com/?msg=fail",# + "/failure/",
            "pending": "https://ascend-store.herokuapp.com/?msg=pending",# + "/pending/"
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
    if request.method == "POST":
        models.MercadoPagoNotification(topic=request.GET['topic'],id_topic=request.GET['id'],json=str(request.POST)).save()
        return HttpResponse(json.dumps(response_data), content_type="application/json", status=201)

    elif request.method == "GET":
        # try:
        #     topic = request.GET['topic']
        #     id = request.GET['id']
        # except:
        #     pass
        # models.MercadoPagoNotification(topic=topic,id_topic=id).save()
        return HttpResponse(status=201)
    else:
        return HttpResponse(status=404)


@login_required
def favoritos_view(request):
    data = {}
    data['favorito'] = models.Favorito.objects.filter(user=request.session['_auth_user_id'])
    data['form_shop_car'] = forms.AddShopCar
    return render(request, 'app/favorito.html', data)

@login_required
def favoritos_view_add(request):
    if request.method == "POST":
        form = forms.FavoritoForm(request.POST)
        if form.is_valid():
            valid = models.Favorito.objects.filter(user=request.POST['user'], produto=request.POST['produto'])
            if valid:
                messages.add_message(request, messages.INFO, "Esse produto já está nos favoritos!")
                return redirect('/')
            else: 
                form.save()
                messages.add_message(request, messages.INFO, "Produto adicionado aos Favoritos!")
                return redirect('/')
        else:
            messages.add_message(request, messages.INFO, "Falha ao adicionar aos Favoritos! Formulário Inválido!")
            return redirect('/')
    else:
        messages.add_message(request, messages.INFO, "Falha ao adicionar aos Favoritos!")
        return redirect('/')

@login_required
def favoritos_view_delete(request):
    if request.method == "POST":
        form = forms.FavoritoForm(request.POST)
        if form.is_valid():
            models.Favorito.objects.filter(id=request.POST['id_favorito'], user=request.POST['user'], produto=request.POST['produto']).delete()
            messages.add_message(request, messages.INFO, "Produto removido dos Favoritos!")
            return redirect('/favoritos/')
        else:
            messages.add_message(request, messages.INFO, "Falha ao remover dos Favoritos! Formulário Inválido!")
            return redirect('/favoritos/')
    else:
        messages.add_message(request, messages.INFO, "Falha ao remover dos Favoritos!")
        return redirect('/favoritos/')

@login_required
def user_account(request):
    return render(request, 'app/user_account.html')