from django.shortcuts import render, redirect,get_object_or_404
from .cart import Cart
from website.models import Product
from django.http import JsonResponse
import json
# Create your views here.
def cart_add(request):
    cart=Cart(request)

    if request.POST.get('action')=='post':
        product_id=int(request.POST.get('product_id'))

        product=get_object_or_404(Product, id=product_id)

        cart.add(product=product)

        cart_qty=cart.__len__()
        response=JsonResponse({'qty': cart_qty, 'cart':json.dumps(cart.get_cart())})

        return response

def cart_delete(request):
    pass

def cart_update(request):
    pass