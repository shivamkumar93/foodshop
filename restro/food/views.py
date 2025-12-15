from django.shortcuts import render
from .serializers import *
from django.contrib.auth.models import User
from .models import *
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from django.core.validators import validate_email
import dns.resolver

# Create your views here.

# class UserRegisterViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserRegisterSerializer
class SingupViewSet(viewsets.ViewSet):
    @action(detail=False, methods=['post'])
    def register(self, request):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response({"error":"Please enter email"}, status=400)
        try:
            validate_email(email)
        except:
            return Response({'error':'not valid email'})
        
        domain = email.split('@')[1]
        try:
            dns.resolver.resolve(domain,'MX')
        except:
            return Response({"error":"please enter valid email"}, status=400)
        
        User.objects.create_user(username=username, email=email, password=password)
        return Response({"message":"user created successfully"},status=200 )
        

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

    