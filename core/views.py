from django.shortcuts import render
from product.models import Product
from .models import *


def index(request):
    data = {
        'title': 'Home | Shopzesta',
        'products': Product.objects.all()[0:8],
        'carousel': Carousel.objects.all(),
    }
    return render(request, 'core/index.html', data)


def about_us(request):
    data = {
        'title': 'About us | Shopzesta',
    }
    return render(request, 'core/about_us.html', data)


def terms_and_conditions(request):
    data = {
        'title': 'Terms and conditions | Shopzesta',
    }
    return render(request, 'core/about_us.html', data)


def payment(request):
    data = {
        'title': 'Payment | Shopzesta',
    }
    return render(request, 'core/payment.html', data)
