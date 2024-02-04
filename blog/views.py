from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')

def index(request):
    return render(request, 'index.html', {})

def about(request):
    return render(request, 'about.html', {})

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

def logOut(request):
    logout(request)
    return redirect('signUp')