import json
import random

import requests
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from requests.auth import HTTPBasicAuth
from rest_framework import viewsets, permissions, status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_200_OK

from commerce.models import *
from commerce.mpesa_credentials import MpesaAccessToken, LipanaMpesaPpassword
from commerce.serializers import *


def getAccessToken(request):
    consumer_key = 'cHnkwYIgBbrxlgBoneczmIJFXVm0oHky'
    consumer_secret = '2nHEyWSD4VjpNh2g'
    api_URL = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
    r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))
    mpesa_access_token = json.loads(r.text)
    validated_mpesa_access_token = mpesa_access_token['access_token']
    return HttpResponse(validated_mpesa_access_token)


def lipa_na_mpesa_online(request):
    access_token = MpesaAccessToken.validated_mpesa_access_token
    api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    headers = {"Authorization": "Bearer %s" % access_token}
    request = {
        "BusinessShortCode": LipanaMpesaPpassword.Business_short_code,
        "Password": LipanaMpesaPpassword.decode_password,
        "Timestamp": LipanaMpesaPpassword.lipa_time,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": 1,
        "PartyA": 254728851119,  # replace with your phone number to get stk push
        "PartyB": LipanaMpesaPpassword.Business_short_code,
        "PhoneNumber": 254728851119,  # replace with your phone number to get stk push
        "CallBackURL": "https://sandbox.safaricom.co.ke/mpesa/",
        "AccountReference": "Henry",
        "TransactionDesc": "Testing stk push"
    }
    response = requests.post(api_url, json=request, headers=headers)
    return HttpResponse('success')


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def get_access_token(request):
    username = request.data.get("consumer_key")
    password = request.data.get("consumer_password")
    if username is None or password is None:
        return Response('Please provide both consumer key and consumer password', status=HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)

    if not user:
        context = {
            'error': 'Invalid Credentials',
        }
        return Response('Invalid Credentials', status=HTTP_400_BAD_REQUEST)
    token, _ = Token.objects.get_or_create(user=user)

    buyer = Buyer.objects.get(user_ptr_id=user.id)
    s = UserSerializer(buyer, many=False)
    context = {
        'token': token.key,
    }
    print(context)
    return Response(context, status=HTTP_200_OK)


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def buyer_sign_up(request):
    username = request.data.get("username", "")
    password = request.data.get("password", "")
    email = request.data.get("email", "")
    first_name = request.data.get("first_name", "")
    last_name = request.data.get("last_name", "")
    phone_number = request.data.get("phone_number", "")
    if not username and not password and not email and not first_name and not last_name:
        return Response(
            data={
                "response": "username, password and email is required to register a user"
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    buyer = Buyer.objects.create(
        username=username,
        password=make_password(password),
        email=email,
        first_name=first_name,
        last_name=last_name,
        is_staff=True,
        phone_number=phone_number
    )
    context = {
        'response': 'User Created Successfully',
        'buyer': buyer
    }
    return Response(context, status=status.HTTP_201_CREATED)


class UserViewSet(viewsets.ModelViewSet):
    queryset = Buyer.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter(low_stock__gt=0)
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]


class ProductCategoryViewSet(viewsets.ModelViewSet):
    queryset = ProductCategory.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [permissions.AllowAny]


class AddressViewSet(viewsets.ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    permission_classes = [permissions.AllowAny]


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        buyer = Buyer.objects.filter(user_ptr_id=self.request.user.id).first()
        return Order.objects.filter(buyer_id=buyer.id)


class OrderItemViewSet(viewsets.ModelViewSet):
    serializer_class = OrderItemSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return OrderItem.objects.filter(order_id=self.kwargs['order_id'])


@csrf_exempt
@api_view(["GET"])
@permission_classes((AllowAny,))
def product_comments(request, product_id):
    comments = ProductReview.objects.filter(product_id=product_id)
    s = ProductReviewSerializer(comments, many=True)

    # context = {
    #     'comments': ,
    # }
    return Response(s.data, status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes((AllowAny,))
def add_to_cart(request, product_id):
    token = Token.objects.get(key=request.META.get('HTTP_AUTHORIZATION').split()[1])
    print(token)
    buyer = Buyer.objects.filter(user_ptr_id=token.user_id).first()
    order = Order.objects.filter(buyer_id=buyer.id, ordered=False).first()
    if order is not None:
        print(order)
        order_item = OrderItem.objects.filter(order_id=order.id, product_id=product_id).first()
        if order_item is not None:
            print(order_item)
            old_quantity = order_item.quantity
            new_quantity = old_quantity + 1
            order_item.quantity = new_quantity
            order_item.save()
            o = OrderSerializer(order, many=False)
            return Response(o.data, status=status.HTTP_200_OK)
        else:
            OrderItem.objects.create(
                order = order,
                quantity=1,
                product_id=product_id
            )
            o = OrderSerializer(order, many=False)
            return Response(o.data, status=status.HTTP_200_OK)
    else:
        order = Order.objects.create(
            buyer_id=buyer.id,
            unique_ref=random.randint(1000, 100000)
        )
        order_item = OrderItem.objects.create(
                order=order,
                quantity=1,
                product_id=product_id
        )
        o = OrderSerializer(order, many=False)
        return Response(o.data, status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes((AllowAny,))
def get_cart(request):

    token = Token.objects.get(key=request.META.get('HTTP_AUTHORIZATION').split()[1])
    print(token)
    buyer = Buyer.objects.filter(user_ptr_id=token.user_id).first()
    order = Order.objects.filter(buyer_id=buyer.id, ordered=False).first()

    pp = PProductSerializer(order.products, many=True)
    print(pp.data)
    return Response(pp.data, status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes((AllowAny,))
def get_profile(request):
    buyer = Buyer.objects.filter(id='').first()
    b = UserSerializer(buyer, many=False)
    return Response(b.data, status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes((AllowAny,))
def get_orders(request):
    token = Token.objects.get(key=request.META.get('HTTP_AUTHORIZATION').split()[1])
    buyer = Buyer.objects.filter(user_ptr_id=token.user_id).first()
    orders = Order.objects.filter(buyer_id=buyer.id)
    o = OrderSerializer(orders, many=True)

    return Response(o.data, status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes((AllowAny,))
def order_products(request, order_id):
    order = Order.objects.get(id=order_id)
    p = ProductSerializer(order.products, many=True)
    return Response(p.data, status=status.HTTP_200_OK)