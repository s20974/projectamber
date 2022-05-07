from django.http import JsonResponse

from products.models import Product
from .serializers import ProductsSerializer

from django.conf import settings

import requests

import re

def user_get_products(request):
    products = ProductsSerializer(
        Product.objects.all().order_by("-id"),
        many = True,
        context = {"request":request},
    ).data

    return JsonResponse({"products": products}) 

def get_phone_code(phone, quantity):
    pattern = r'^[+]{1}[(]{0,1}([0-9]{%s})[)]{0,1}.*' % (quantity)
    match = re.search(pattern, phone)

    return match.group(1)

def  user_get_product(request, product_id):
    product = ProductsSerializer(
        Product.objects.filter(id=product_id),
        many = True,
        context = {"request":request},
    ).data
    return JsonResponse({"product":product})


def send_verfication_code(user):
    data = {
        'api_key': settings.AUTHY_KEY,
        'via': 'sms',
        'country_code': get_phone_code(user.phone, 2),
        'phone_number': user.phone,
    }
    url = 'https://api.authy.com/protected/json/phones/verification/start'
    response = requests.post(url,data=data)
    return response

def verify_sent_code(one_time_password, user):
    data= {
        'api_key': settings.AUTHY_KEY,
        'country_code': get_phone_code(user.phone, 2),
        'phone_number': user.phone,
        'verification_code': one_time_password,
    }
    url = 'https://api.authy.com/protected/json/phones/verification/check'
    response = requests.get(url,data=data)
    return response
