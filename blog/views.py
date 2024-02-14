import base64
from io import BytesIO
import requests
from http.client import REQUEST_ENTITY_TOO_LARGE, REQUEST_HEADER_FIELDS_TOO_LARGE, REQUEST_TIMEOUT
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
import matplotlib.pyplot as plt

from . import models

@login_required(login_url='login')

def index(request):
    return render(request, 'index.html', {})

def signUp(request):
    if request.method=='POST':
        name=request.POST.get('name')
        username=request.POST.get('username')
        email=request.POST.get('email')
        password=request.POST.get('password')
        passwordConfirm=request.POST.get('passwordConfirm')
        
        if password!=passwordConfirm:
            return HttpResponse('Your passwords do not match, try again.')
        else:
            my_user=User.objects.create_user(username, email, password)
            my_user.save()
            print(name, username, email, password)
            return redirect('login')
        
    return render(request, 'signUp.html', {})

def logIn(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        print( username, password)
        user=authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            return HttpResponse('Username or password is incorrect.')
        
    return render(request, 'logIn.html', {})

def forum(request):
    return render(request, 'forum.html', {})

def news(request):
    data = {'2023': 144444359, '2022': 144713314, '2020': 145617329, '2015': 144668389, '2010': 143242599, '2000': 146844839}
    names = list(data.keys())[::-1]
    values = list(data.values())[::-1]

    plt.plot(names, values, linestyle = 'dotted')
        
    buf = BytesIO()
    plt.savefig(buf, format='png', dpi=300)
    image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8').replace('\n', '')
    buf.close()
    
    all_entries = models.Content.objects.filter(country = "Sri Lanka")
    return render(request, 'news.html', {"image_base64": image_base64, "content": all_entries})

def profile(request):
    return render(request, 'profile.html', {})

def settings(request):
    return render(request, 'settings.html', {})

def logOut(request):
    logout(request)
    return redirect('signUp')

# def news(request):
#     api_url = 'https://api.api-ninjas.com/v1/country?name=Russia'
#     headers = {'X-Api-Key': 'ZLPOykr1PiSkaMTpZxUYPg==1qes8BJwWRpO0GQl'}

#     response = requests.get(api_url, headers=headers)
    
#     if response.status_code == requests.codes.ok:
#         data = response.json()
#         population = data[0]['population']
#         return render(request, 'news.html', {'population': population})
#     else:
#         return JsonResponse({'error': 'Failed to fetch data'}, status=500)

