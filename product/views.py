from django.shortcuts import render, redirect
from .models import *


def overview(request, id):
    product = Product.objects.get(pk=id)
    data = {
        'title': product.name + ' | Shopzesta',
        'product': product,
    }
    return render(request, 'product/overview.html', data)


def products(request):
    num_of_query = 9
    page = int(request.GET.get('page')) if request.GET.get('page') else 1

    print(num_of_query, page)

    data = {
        'title': 'Shop | Shopzesta',
        'products': Product.objects.all()[(page-1)*num_of_query: page*num_of_query],
        'page': page,
        'prev_page': page - 1,
        'prev_page2': page - 2,
        'prev_page3': page - 3,
        'next_page': page + 1,
        'next_page2': page + 2,
        'next_page3': page + 3,
    }
    return render(request, 'product/products.html', data)


def cart(request):
    if not request.user.is_authenticated:
        return redirect('user:login')

    cart = Cart.objects.filter(user=request.user).first()
    data = {
        'title': 'Cart | Shopzesta',
        'cart': cart,
        'cart_items': CartItem.objects.filter(cart=cart)
    }

    if request.method == 'GET':
        return render(request, 'product/cart.html', data)

    if request.method == 'POST':
        product = Product.objects.get(pk=request.POST['product'])
        quantity = int(request.POST['quantity'])
        cart_item = CartItem.objects.filter(product=product).first()

        cur_quantity = cart_item.quantity if cart_item else 0

        if product.count_in_stock - quantity - cur_quantity < 0:
            data['error'] = 'Not enough stock'
            return render(request, 'product/cart.html', data)

        cart_item.quantity += quantity

        if cart_item.quantity == 0:
            cart_item.delete()
        else:
            cart_item.save()

        return redirect('product:cart')


def add_to_cart(request):
    if not request.user.is_authenticated:
        return redirect('user:login')

    if request.method == 'POST':
        product = Product.objects.get(pk=request.POST['product'])
        quantity = int(request.POST['quantity'])
        qty_abs = request.POST.get('qty_abs')

        cart = Cart.objects.filter(user=request.user).first()
        cart_item = CartItem.objects.filter(
            product=product, cart=cart).first()

        if product.count_in_stock - quantity < 0:
            data = {
                'title': 'Cart | Shopzesta',
                'cart': cart,
                'cart_items': CartItem.objects.filter(cart=cart),
                'error': 'Not enough stock',
            }
            return render(request, 'product/cart.html', data)

        if cart is None:
            cart = Cart(user=request.user)
            cart.save()

        if cart_item is None:
            cart_item = CartItem(product=product, quantity=quantity, cart=cart)
            cart_item.save()
        else:
            if qty_abs:
                cart_item.quantity = quantity
            else:
                cart_item.quantity += quantity

            cart_item.save()

        return redirect('core:index')


def create_order(request):
    if not request.user.is_authenticated:
        return redirect('user:login')

    if request.method == 'POST':
        cart = Cart.objects.filter(user=request.user).first()

        if cart is None:
            return redirect('product:products')

        # Checking count in stock
        cart_items = CartItem.objects.filter(cart=cart)

        for cart_item in cart_items:
            if cart_item.product.count_in_stock < cart_item.quantity:
                data = {
                    'title': 'Cart | Shopzesta',
                    'cart': cart,
                    'cart_items': cart_items,
                    'error': 'Not enough stock',
                }
                return render(request, 'product/cart.html', data)

        order = Order(user=request.user, total_price=cart.total_price)
        order.save()

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


def remove_from_cart(request):
    if not request.user.is_authenticated:
        return redirect('user:login')

    if request.method == 'POST':
        product = Product.objects.get(pk=request.POST['product'])
        cart = Cart.objects.filter(user=request.user).first()

        cart_item = CartItem.objects.filter(
            product=product, cart=cart).first()

        if cart_item:
            cart_item.delete()

        cart_item = CartItem.objects.filter(cart=cart).first()

        if cart_item is None:
            cart.delete()

        return redirect('product:cart')
