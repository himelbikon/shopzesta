from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from .models import User


def index(request):
    return render(request, 'user/index.html')


def user_login(request):
    data = {
        'title': 'Login | Shopzesta',
    }

    if request.user.is_authenticated:
        return redirect('core:index')

    if request.method == 'GET':
        return render(request, 'user/login.html', data)

    if request.method == 'POST':
        user = authenticate(
            request,
            email=request.POST['email'],
            password=request.POST['password']
        )

        if user:
            login(request, user)
            return redirect('core:index')
        else:
            data['error'] = 'Invalid email or password!'
            return render(request, 'user/login.html',  data)


def user_logout(request):
    if request.user.is_authenticated and request.method == 'POST':
        logout(request)

    return redirect('core:index')


def user_register(request):
    data = {
        'title': 'Register | Shopzesta',
    }

    if request.user.is_authenticated:
        return redirect('core:index')

    if request.method == 'GET':
        return render(request, 'user/register.html', data)

    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if User.objects.filter(email=email).exists():
            data['error'] = 'Email already exists!'
            return render(request, 'user/register.html', data)

        if password != password2:
            data['error'] = 'Passwords do not match!'
            return render(request, 'user/register.html', data)

        user = User.objects.create_user(email=email, password=password)
        user.save()

        login(request, user)

        return redirect('core:index')
