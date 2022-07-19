from django.shortcuts import render
from product.models import Product


def index(request):
    data = {
        'products': Product.objects.all()[0:8]
    }
    return render(request, 'core/index.html', data)
