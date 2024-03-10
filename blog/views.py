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
from django.contrib import messages
from .decorators import unauthenticated_user

from . import models

@login_required(login_url='login')
def index(request):
    username = request.user.username  # this takes the logged in username and used for the "Hello, username" in the navbar
    return render(request, 'index.html', {'username': username})

@unauthenticated_user
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
            my_user=User.objects.create_user(name, username, email, password)
            my_user.save()
            messages.success(request, 'Your account was created successfully, ' +username)
            return redirect('login')
        
    return render(request, 'signUp.html', {})

@unauthenticated_user
def logIn(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.info(request, 'Username or password is incorrect.')
        
    return render(request, 'logIn.html', {})

def forum(request):
    return render(request, 'forum.html', {})

def russia(request):
    data = {'2023': 144444359, '2022': 144713314, '2020': 145617329, '2015': 144668389, '2010': 143242599, '2000': 146844839}
    names = list(data.keys())[::-1]
    values = list(data.values())[::-1]

    plt.figure()
    plt.plot(names, values, linestyle='dotted')

    buf = BytesIO()
    plt.savefig(buf, format='png', dpi=300)
    image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8').replace('\n', '')
    buf.close()

    all_entries = models.Content.objects.filter(country="Russia")
    return render(request, 'russia.html', {"image_base64": image_base64, "content": all_entries})

def palestine(request):
    data = {'2023': 5371230, '2022': 5250072, '2020': 5019401, '2015': 4484614, '2010': 3992278, '2000': 3139954}
    names = list(data.keys())[::-1]
    values = list(data.values())[::-1]

    plt.figure()
    plt.plot(names, values, linestyle='dotted')

    buf = BytesIO()
    plt.savefig(buf, format='png', dpi=300)
    image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8').replace('\n', '')
    buf.close()

    all_entries = models.Content.objects.filter(country="Sri Lanka")
    return render(request, 'palestine.html', {"image_base64": image_base64, "content": all_entries})

def zimbabwe(request):
    data = {'2023': 16665409, '2022': 16320537, '2020': 15669666, '2015': 14154937, '2010': 12839771, '2000': 11834676}
    names = list(data.keys())[::-1]
    values = list(data.values())[::-1]

    plt.figure()
    plt.plot(names, values, linestyle='dotted')

    buf = BytesIO()
    plt.savefig(buf, format='png', dpi=300)
    image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8').replace('\n', '')
    buf.close()

    all_entries = models.Content.objects.filter(country="Zimbabwe")
    return render(request, 'zimbabwe.html', {"image_base64": image_base64, "content": all_entries})

def news(request):
    return render(request, 'news.html', {}) 

def profile(request):
    return render(request, 'profile.html', {})

def settings(request):
    return render(request, 'settings.html', {})

def logOut(request):
    logout(request)
    return redirect('logIn')

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

