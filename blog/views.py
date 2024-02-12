import requests
from http.client import REQUEST_ENTITY_TOO_LARGE, REQUEST_HEADER_FIELDS_TOO_LARGE, REQUEST_TIMEOUT
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse

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

# def forum(request):
#     return render(request, 'forum.html', {})

# def news(request):
#     return render(request, 'news.html', {})

# def profile(request):
#     return render(request, 'profile.html', {})

# def settings(request):
#     return render(request, 'settings.html', {})

def logOut(request):
    logout(request)
    return redirect('signUp')

# def index(request):
#     api_url = 'https://api.api-ninjas.com/v1/country?name=Russia'
#     headers = {'X-Api-Key': 'ZLPOykr1PiSkaMTpZxUYPg==1qes8BJwWRpO0GQl'}

#     response = requests.get(api_url, headers=headers)
    
#     if response.status_code == requests.codes.ok:
#         data = response.json()
#         population = data[0]['population']
#         return render(request, 'index.html', {'population': population})
#     else:
#         return JsonResponse({'error': 'Failed to fetch data'}, status=500)

