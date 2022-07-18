from django.urls import path
from .views import *

app_name = 'product'

urlpatterns = [
    path('', overview, name='overview'),
    path('products/', products, name='products'),
    path('cart/', cart, name='cart'),

    path('add_to_cart/', add_to_cart, name='add_to_cart'),
]
