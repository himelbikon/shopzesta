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
