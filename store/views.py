from django.shortcuts import render,HttpResponse
from django.http import JsonResponse
from .models import *
import json
import datetime
from .utils import cookieCart,cartData,guestOrder
from django.views.generic import DetailView

def store(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            productId = data.get('productId')
            print('productId:', productId)

            if productId is not None:
                product = Product.objects.get(id=productId)
                print('productId:', product.brand)
                response_data = {'product_brand': product.brand,
                                 'product_category':product.category,
                                 'product_price':product.price,
                                 'product_description': product.description,
                                 'product_image':product.image.url}

                return JsonResponse(response_data, safe=False)
        
                data = cartData(request)
                cartItems = data['cartItems']
                order = data.get('order', None)
                items = data.get('items', [])

                products = Product.objects.all()
                context = {
                    'products': products,
                    'cartItems': cartItems,
                    'items': items,
                    
                }
                

                return render(request, "store/store.html", context)
            else:
                return HttpResponse('Missing productId', status=400)

        except json.JSONDecodeError as e:
            return HttpResponse(str(e), status=400)
    elif request.method == 'GET':
        # Handle GET requests here
        products = Product.objects.all()
        context = {
            'products': products,
        }
        return render(request, "store/store.html", context)
    
    # Handle other request methods if needed
    return HttpResponse('Method Not Allowed', status=405)

class PostDetailView(DetailView):
    model = Product

def cart(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    context = {
        'items':items,'order':order,'cartItems':cartItems
    }
    return render(request,"store/cart.html",context)


def checkout(request):
    
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context ={
        'items':items,
        'order':order,
        'cartItems':cartItems,
    }

    return render(request,"store/checkout.html",context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action =data['action']

    print('Action:',action)
    print('productId:',productId)

    customer =request.user.customer
    product = Product.objects.get(id=productId)
    order, created=Order.objects.get_or_create(customer=customer,complete=False)

    orderItem, created =OrderItem.objects.get_or_create(order=order,product=product)
    if action == 'add':
        orderItem.quantity =(orderItem.quantity + 1)
    elif action =='remove':
        orderItem.quantity =(orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('item was added',safe=False)

def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
    else:
        customer, order = guestOrder(request, data)

    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == float(order.get_cart_total):
        order.complete = True
    order.save()

    if order.shipping:
        try:
            # Attempt to retrieve the shipping address for the user
            shipping_address = ShippingAddress.objects.get(customer=customer)
        except ShippingAddress.DoesNotExist:
            # If the shipping address doesn't exist, initialize it as None
            shipping_address = None

        if shipping_address:
            # Update the existing shipping address
            shipping_address.address = data['shipping']['address']
            shipping_address.city = data['shipping']['city']
            shipping_address.state = data['shipping']['state']
            shipping_address.zipcode = data['shipping']['zipcode']
        else:
            # Create a new shipping address
            shipping_address = ShippingAddress(
                customer=customer,
                order=order,
                address=data['shipping']['address'],
                city=data['shipping']['city'],
                state=data['shipping']['state'],
                zipcode=data['shipping']['zipcode'],
            )
        shipping_address.save()

    return JsonResponse("payment complete", safe=False)