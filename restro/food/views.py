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


# class SingupViewSet(viewsets.ViewSet):
#     @action(detail=False, methods=['post'])
#     def register(self, request):
#         username = request.data.get('username')
#         email = request.data.get('email')
#         password = request.data.get('password')

#         if not email or not password:
#             return Response({"error":"Please enter email"}, status=400)
#         try:
#             validate_email(email)
#         except:
#             return Response({'error':'not valid email'})
        
#         domain = email.split('@')[1]
#         try:
#             dns.resolver.resolve(domain,'MX')
#         except:
#             return Response({"error":"please enter valid email"}, status=400)
        
#         User.objects.create_user(username=username, email=email, password=password)
#         return Response({"message":"user created successfully"},status=200 )

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
                message="your otp {otp}",
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
            verify_otp = User.objects.filter(email=email, otp=otp, is_varified = False).latest
        except:
            return Response({'message':'invalid otp'})
        
        verify_otp.is_verified = True
        verify_otp.save()
        return Response({'message':'otp verified successfully'})


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

    