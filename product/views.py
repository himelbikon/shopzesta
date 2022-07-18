from django.shortcuts import render, redirect
from .models import *


def overview(request, id):
    data = {
        'product': Product.objects.get(pk=id)
    }
    return render(request, 'product/overview.html', data)


def products(request):
    data = {
        'products': Product.objects.all()
    }
    return render(request, 'product/products.html', data)


def cart(request):
    if not request.user.is_authenticated:
        return redirect('user:login')

    if request.method == 'GET':
        print('cart cart ===============')
        cart = Cart.objects.filter(user=request.user).first()
        data = {
            'cart': cart,
            'cart_items': CartItem.objects.filter(cart=cart)
        }

        return render(request, 'product/cart.html', data)


def add_to_cart(request):
    if not request.user.is_authenticated:
        return redirect('user:login')

    if request.method == 'POST':
        print('===================================')
        print(request.POST)
        print('===================================')
        product = Product.objects.get(pk=request.POST['product'])
        quantity = int(request.POST['quantity'])

        cart = Cart.objects.filter(user=request.user).first()

        if cart is None:
            cart = Cart(user=request.user)
            cart.save()

        cart_item = CartItem.objects.filter(
            product=product, cart=cart).first()

        if cart_item is None:
            cart_item = CartItem(product=product, quantity=quantity, cart=cart)
            cart_item.save()
        else:
            cart_item.quantity += quantity
            cart_item.save()

        return redirect('core:index')


def create_order(request):
    print('======================================')
    print('Create Order')
    print('======================================')
    if not request.user.is_authenticated:
        return redirect('user:login')

    if request.method == 'POST':
        cart = Cart.objects.filter(user=request.user).first()

        if cart is None:
            return redirect('product:products')

        order = Order(user=request.user, total_price=cart.total_price)
        order.save()

        cart_items = CartItem.objects.filter(cart=cart)

        for item in cart_items:
            order_item = OrderItem(
                order=order,
                product=item.product,
                quantity=item.quantity,
                qty_price=item.qty_price
            )
            order_item.save()

        cart.delete()

    return redirect('core:index')
