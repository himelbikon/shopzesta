from django.shortcuts import render, redirect
from .models import *
from product.models import Product


def overview(request):
    pass


def products(request):
    data = {
        'products': Product.objects.all()
    }
    return render(request, 'product/products.html', data)


def cart(request):
    if not request.user.is_authenticated:
        return redirect('user:login')

    return render(request, 'product/cart.html')


def add_to_cart(request):
    if not request.user.is_authenticated:
        return redirect('user:login')

    if request.method == 'POST':
        product = request.POST['product']
        quantity = request.POST['quantity']

        cart_item = CartItem.objects.filter(
            user=request.user, product=product).first()

        if cart_item:
            cart_item.quantity += int(quantity)
            cart_item.save()
        else:
            new_cart_item = CartItem(
                user=request.user, product=Product.objects.get(pk=product), quantity=quantity)
            new_cart_item.save()

        return redirect('core:index')
