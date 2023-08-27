from django.shortcuts import render,redirect
from product.models import Category,Product,Order
import stripe
import json
from users.models import User

stripe.api_key = 'sk_test_tR3PYbcVNZZ796tH88S4VQ2u'

# Create your views here.
def homePage(request):
    # cart=request.session.get('cart')
    # if cart:
    #     request.session.get('cart').clear()
    # else:
    #     cart={}
    if request.method == 'POST':
        product = request.POST.get('product')
        cart = request.session.get('cart')
        if cart:
            quantity = cart.get(product)
            if quantity:
                cart[product]=quantity+1
            else:
                cart[product]=1
        else:
            cart={}
            cart[product]=1
        request.session['cart']=cart
    categories = Category.objects.all()
    return render(request,"home/homePage.html",{"categories":categories})

def success(request):
    order_data = request.session.get('order_data')

    # Create and save the order using the order_data
    if order_data:
        customer = order_data['customer']
        address = order_data['address']
        phone = order_data['phone']
        product_ids = order_data['products']
        cart = request.session.get('cart')
        total_amount = order_data['total_amount']

        products = Product.objects.filter(id__in=product_ids)
        for product in products:
            order = Order(
                customer=User(id=customer),
                product=product,
                price=product.price,
                address=address,
                phone=phone,
                quantity=cart.get(str(product.id))
            )
            order.save()

    del request.session['order_data']
    request.session['cart']={}
    return render(request,'success.html')

def cancel(request):
    return render(request,'cancel.html')