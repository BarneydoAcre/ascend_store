from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

def home(request):
    return render(request, 'app/home.html')

@login_required
def users(request):
    data = {}
    data['users'] = User.objects.all()
    return render(request, 'app/user.html', data)