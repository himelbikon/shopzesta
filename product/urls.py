from django.urls import path
from .views import *

app_name = 'product'

urlpatterns = [
    path('', products, name='products'),
    path('<int:id>/', overview, name='overview'),
    path('cart/', cart, name='cart'),

    path('create_order/', create_order, name='create_order'),

    path('add_to_cart/', add_to_cart, name='add_to_cart'),
]
