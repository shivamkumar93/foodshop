from django.shortcuts import render
from .serializers import *
from django.contrib.auth.models import User
from .models import *
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from django.core.validators import validate_email
from rest_framework.views import APIView
import dns.resolver
import random
from django.core.mail import send_mail
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from google.oauth2 import id_token
from google.auth.transport import requests
from django.conf import settings

class RegisterAPI(APIView):

    def post(self, request):
        
        data = request.data
        serializer = UserRegisterSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save(is_varified=False)
            
            otp = random.randint(100000, 999999)
            user.otp = otp
            
            user.save()

    # send otp on email
            send_mail(
                subject="email verification otp",
                message=f"your otp {otp}",
                from_email="bcashivam11@gmail.com",
                recipient_list=[user.email],
                fail_silently=False
            )
            return Response({"message": "User registered successfully"},status=201)
        else:
            return Response(serializer.errors, status=400)
        
class VerifyOtp(APIView):
    def post(self, request):
        email = request.data.get('email')
        otp = request.data.get('otp')

        if not email or not otp:
            return Response({'message':'Please enter valid email or otp'}, status=400)
        
        try:
            verify_otp = User.objects.filter(email=email, otp=otp).last()
        except:
            return Response({'message':'invalid otp'})
        
        if verify_otp.is_varified == False:

            verify_otp.is_varified = True
            verify_otp.save()
    
        return Response({'message':'otp verified successfully'})


class LoginAPIView(viewsets.ViewSet):
    @action(detail=False, methods=['post'])
    def login(self, request):

        email = request.data.get('email')
        password = request.data.get('password')
        if not email or not password :
            return Response({'error':" email or password required"}, status=400)
        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'error':'user is not available'},status=400)
        
        if not user.check_password(password):
            return Response({'error':'email or password invalid'},status=400)
        
        token, create = Token.objects.get_or_create(user=user)

        return Response({'message':'token created successfully', 'token':token.key, 'email':user.email})
    
    @action(detail=False, methods=['post'])
    def google_login(self, request):

        google_token = request.data.get('id_token')

        if not google_token:
            return Response({'error':'google token is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            idinfo = id_token.verify_oauth2_token(google_token, requests.Request(), settings.GOOGLE_CLIENT_ID)
           
        except ValueError:
            return Response({'error':'invalid google token'}, status=status.HTTP_400_BAD_REQUEST)
        
        email = idinfo['email']
        user, create = User.objects.get_or_create(email=email)

        token, create = Token.objects.get_or_create(user=user)
        return Response({'message':'user create successfully ',
                        "token":token.key,
                        "email":user.email,
                        "login_type":"google"
                        })
            

    

        
class ForgotPasswordView(viewsets.ViewSet):
    @action(detail=False, methods=['post'])
    def reset_otp(self, request):
        email = request.data.get('email')
        if not email:
            return Response({'error':'email required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = User.objects.filter(email=email).first()
        except User.DoesNotExist:
            return Response({'error':'email invalid'}, status=400)
        
        otp = random.randint(100000, 999999)

        user.otp = otp
        user.save()
        
        send_mail(
            subject="forgot password",
            message=f"new otp {otp}",
            from_email="bcashivam11@gmail.com",
            recipient_list=[user.email],
            fail_silently=False

        )
        return Response({'message':'sent forgot password otp'}, status=201)
    @action(detail=False, methods=['post'])
    def reset_password(self , request):
        email = request.data.get('email')
        otp = request.data.get('otp')
        new_password = request.data.get('new_password')

        if not email or not otp or not new_password:
            return Response({'error':'invalid email otp and new_password'})
        
        try:
            user = User.objects.filter(email=email).first()
        except User.DoesNotExist:
            return Response({'error':'invalid email'}, status=400)
        
        if user.otp != otp:
            return Response({'message':'invalid otp'}, status=400)
        
        user.set_password(new_password)
        user.otp = None
        user.save()
        return Response({'message':'your password is change successfully.'})


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

class OrderViewSet(viewsets.ViewSet):
    @action(detail=False, methods=['post'])
    def create_order(self, request):

        data = request.data

        if isinstance(data,dict):
            data = [data]

        serializer = OrderItemSerializer(data=data, many=True)
        serializer.is_valid(raise_exception=True)
        items = serializer.validated_data
        
        if len(items) == 0:
            return Response({'error':'recipe_id or quantity is required'}, status=status.HTTP_400_BAD_REQUEST)
        # order create---
        order = Order.objects.create(user=request.user)

        # orderitmes create--
        for item in items:
            recipe = Recipe.objects.get(id=item['recipe_id'])
            OrderItems.objects.create(order=order, recipe=recipe, quantity = item['quantity'])

        items = [items]
        return Response({'message':'order create successfully', 'order_id':order.id,'total_price':order.get_total_price(),'recipe':items }, status=status.HTTP_201_CREATED)

    