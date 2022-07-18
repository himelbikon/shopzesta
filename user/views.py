from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate


def index(request):
    return render(request, 'user/index.html')


def user_login(request):
    data = {}

    if request.user.is_authenticated:
        return redirect('core:index')

    if request.method == 'GET':
        return render(request, 'user/login.html')

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
