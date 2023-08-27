from django.shortcuts import render,redirect
from .models import Product,Order,ReturnOrder
from users.models import User
from django.contrib.auth.decorators import login_required
import json

import stripe
# This is a public sample test API key.
# Don’t submit any personally identifiable information in requests made with this key.
# Sign in to see your own test API key embedded in code samples.
stripe.api_key = 'sk_test_tR3PYbcVNZZ796tH88S4VQ2u'

# Create your views here.
def productPage(request,c_id):
    products = Product.objects.filter(category=c_id)
    return render(request,"home/productPage.html",{"products":products})

def cartPage(request):
    products=None
    if request.method == 'POST':
        product = request.POST.get('product')
        remove = request.POST.get('remove')
        cart = request.session.get('cart')
        # print(product,remove,cart)
        if cart:
            quantity = cart.get(product)
            print(quantity)
            if quantity!=0:
                # print('hello1')
                if remove=='True':
                    if quantity<=1:
                        cart.pop(product)
                    else:
                        cart[product]  = quantity-1
                else:
                    # print('hello')
                    cart[product]  = quantity+1
                    print(cart[product])
            request.session['cart'] = cart
            return redirect('cartPage')

    if request.session.get('cart'):
        ids = list(request.session.get('cart').keys())
        products = Product.objects.filter(id__in=ids)
        # print(products)
    return render(request,"home/cartPage.html",{"products":products})

YOUR_DOMAIN = "https://cyclestore-d946.onrender.com"
YOUR_SUCCESS_URL = YOUR_DOMAIN+'/success'
YOUR_CANCEL_URL = YOUR_DOMAIN+'/cancel'

@login_required(login_url="/users/login/")
def orderPage(request):
    if request.method == 'POST':
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        customer = request.session.get('customer')
        cart = request.session.get('cart')
        products = Product.objects.filter(id__in=list(cart.keys()))
        
        sum = 0
        for product in products:
            quantity = cart.get(str(product.id))
            sum += quantity * product.price
            
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    'price_data': {
                        'currency': "INR",
                        'unit_amount': sum * 100,
                        'product_data': {
                            'name': "xyz",
                        },
                    },
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=YOUR_SUCCESS_URL,
            cancel_url=YOUR_CANCEL_URL,
        )
        
        # Store order-related data in session for later use after payment
        request.session['order_data'] = {
            'customer': customer,
            'address': address,
            'phone': phone,
            'products': [product.id for product in products],
            'total_amount': sum,
        }
        
        return redirect(checkout_session.url, code=303)

    orders = Order.objects.filter(customer=request.user)
    return render(request, "home/orderPage.html", {"orders": orders})

# Stripe success webhook handler
# def stripe_webhook(request):
    

@login_required(login_url="/users/login/")
def returnorderPage(request,pk):
    order_id = pk
    order = Order.objects.get(id=order_id)
    if request.method == 'POST':
        name = request.POST.get('name')
        contact = request.POST.get('contact')
        damage_des = request.POST.get('damage_desc')
        damage_photo = request.FILES['damage_photo']
        order.is_returned=True
        order.save()
        returnorder=ReturnOrder(name=name,phone=contact,product=Product(id=order.product.id),image=damage_photo,desc=damage_des,customer=User(id=request.user.id))
        returnorder.save()
        return redirect('homePage')
    return render(request,'home/returnorderPage.html',{"order":order})
