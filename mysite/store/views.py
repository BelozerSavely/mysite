from django.shortcuts import render
from django.http import JsonResponse
import json
import datetime

from .models import *
from .utils import cookieCart, cartData, guestOrder


def store(request):
    data = cartData(request)
    cartItems = data['cartItems']

    products = Product.objects.all()
    context = {'products': products, 'cartItems': cartItems}
    return render(request, 'store/store.html', context)


def cart(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/cart.html', context)


def chekout(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/checkout.html', context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print('action:', action)
    print('productId:', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)


def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)

    else:
        customer, order = guestOrder(request, data)

    total = float(data['form']['total'].replace(',', '.'))
    order.transaction_id = transaction_id

    if total == order.get_cart_total:
        order.complete = True
    order.save()

    if order.shipping is True:
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zipcode=data['shipping']['zipcode'],
        )

    return JsonResponse('paypal good', safe=False)


def category_list(request):
    data = cartData(request)
    cartItems = data['cartItems']

    categories = Category.objects.all()
    return render(request, 'store/categories.html', {'categories': categories, 'cartItems': cartItems})


def get_store_by_categories(request, category_id):
    data = cartData(request)
    cartItems = data['cartItems']

    products = Product.objects.filter(category__id=category_id)
    context = {'products': products, 'cartItems': cartItems}
    return render(request, 'store/store.html', context)


def about(request):
    data = cartData(request)
    cartItems = data['cartItems']

    return render(request, 'store/about.html', {'cartItems': cartItems})


def description_page(request, product_id):
    data = cartData(request)
    cartItems = data['cartItems']

    item = Product.objects.get(id=product_id)
    return render(request, 'store/description_page.html', {'item': item, 'cartItems': cartItems})

def contacts(request):
    data = cartData(request)
    cartItems = data['cartItems']

    return render(request, 'store/contacts.html', {'cartItems': cartItems})
