import json
from .models import *
from django.conf import settings


def cookieCart(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}  

    items = []
    order = {'get_cart_total': 0, 'get_cart_items': 0}

    for product_id, cart_item in cart.items():
        try:
            product = Product.objects.get(id=product_id)
            total = product.price * cart_item['quantity']
            
            # Update the order total and cart items count
            order['get_cart_total'] += total
            order['get_cart_items'] += cart_item['quantity']

            # Create a dictionary for the cart item
            item = {
                'product': {
                    'id': product.id,
                    'category': product.category,
                    'brand': product.brand,
                    'price': product.price,
                    'description': product.description,
                    'imageURL': product.imageURL,
                    'image1': product.image1.url if product.image1 else None,
                    'image2': product.image2.url if product.image2 else None,
                    'image3': product.image3.url if product.image3 else None,
                    'image4': product.image4.url if product.image4 else None,
                },
                'quantity': cart_item['quantity'],
                'get_total': total,
            }
            items.append(item)
        except Product.DoesNotExist:
            pass  # Handle the case where a product with the given ID does not exist

    return {'items': items, 'order': order, 'cartItems': order['get_cart_items']}



def cartData(request):
    cartItems = 0 
    
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems=order.get_cart_items
    else:
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']
        order = cookieData['order']
        items = cookieData['items']

    return {'items': items, 'order': order, 'cartItems': cartItems}



def guestOrder(request,data):
    print("user is not logged in...")
                
    print('COOIES:' , request.COOKIES)
    name = data['form']['name']
    email = data['form']['email']

    cookieData = cookieCart(request)
    items = cookieData['items']

    customer,created = Customer.objects.get_or_create(
        email=email,
    )
    customer.name= name
    customer.save()

    order = Order.objects.create(
        customer = customer,
        complete= False,
    )

    for item in items:
        product = Product.objects.get(id = item['product']['id'])

        orderItem = OrderItem.objects.create(
            product =product,
            order = order,
            quantity = item['quantity']
        )
    return customer,order