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

class RegisterAPI(APIView):

    def post(self, request):
        
        data = request.data
        serializer = UserRegisterSerializer(data=data)
        if serializer.is_valid():
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


class LoginAPIView(APIView):
    def post(self, request):

        email = request.data.get('email')
        password = request.data.get('password')
        print(email)
        print(password)

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
        

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

    