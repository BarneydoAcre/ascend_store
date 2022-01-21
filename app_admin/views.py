from django.shortcuts import render

def produtos(request):
    data = {}
    data['msg'] = "Teste"
    return render(request, 'app_admin/produtos.html', data)