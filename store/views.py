from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
import json
import datetime

from .models import *
from .utils import cartData, guestOrder

# Create your views here.

def store(request):
    data = cartData(request)
    cartItems = data['cartItems']
    

    products = Product.objects.all()
    
    banners = textBanner.objects.all()
    context = {'products': products, 'cartItems': cartItems, 'banners': banners}
    return render(request, 'store/store.html', context)

def cart(request):
    data = cartData(request)
    items = data['items']
    order = data['order']
    cartItems = data['cartItems']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/cart.html', context)

def checkout(request):
    data = cartData(request)
    items = data['items']
    order = data['order']
    cartItems = data['cartItems']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/checkout.html', context)

def product_view(request, id):
    product = get_object_or_404(Product, id=id)
    
    data = cartData(request)
    items = data['items']
    order = data['order']
    cartItems = data['cartItems']

    context = {'product': product, 'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/product_view.html', context)

def login_view(request):
    data = cartData(request)
    cartItems = data['cartItems']
    
    context = {'cartItems': cartItems}
    return render(request, 'store/login.html', context)

def processLogin(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                Customer.objects.get_or_create(user=user)
                return JsonResponse({'result': 'Success'})
            else:
                return JsonResponse({'result': 'Account is inactive'})
        else:
            return JsonResponse({'result': 'Wrong username or password'})
    else:
        return JsonResponse({'result': 'Invalid request method'})
    
def processLogout(request):
    if request.method == 'POST':
        logout(request)
        return JsonResponse({'result': 'Success'})
    else:
        return JsonResponse({'result': 'Invalid request method'})
    
def register_view(request):
    data = cartData(request)
    cartItems = data['cartItems']
    
    context = {'cartItems': cartItems}
    return render(request, 'store/register.html', context)

def register(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        
        if User.objects.filter(username=username).exists():
            return JsonResponse({'result': 'A user with this username already exists'})
        
        user = User.objects.create_user(username, email, password)
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        Customer.objects.get_or_create(user=user)
        return JsonResponse({'result': 'Success'})
    else:
        return JsonResponse({'result': 'Invalid request method'})

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action:', action)
    print('ProductId:', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action=='add':
        orderItem.quantity = orderItem.quantity+1
    elif action=='remove':
        orderItem.quantity = orderItem.quantity-1
    orderItem.save()

    if orderItem.quantity <=0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)

def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        print('User is logged in')
        customer=request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)

    else:
        print('User is not logged in...')
        print('COOKIES:', request.COOKIES)
        customer, order = guestOrder(request, data)
            
    total=float(data['form']['total'])
    order.transaction_id=transaction_id

    print('total:', total, 'order.get_cart_total:', float(order.get_cart_total))
    if total == float(order.get_cart_total):
        print('Order Complete')
        order.complete=True
    order.save()
    
    if order.shipping==True:
        ShippingAddress.objects.create(
                customer=customer,
                order=order,
                address=data['shipping']['address'],
                city=data['shipping']['city'],
                state=data['shipping']['state'],
                zipcode=data['shipping']['zipcode'],
            )
    
    return JsonResponse('Payment complete', safe=False)