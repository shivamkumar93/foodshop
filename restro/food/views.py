from django.shortcuts import render
from .serializers import *
from django.contrib.auth.models import User
from .models import *
from rest_framework import viewsets
from rest_framework.response import Response

# Create your views here.

class UserRegisterViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

    # def create(self):
    #     recipe = Recipe.objects.get(id=id)
    #     recipe.is_veg = True
    #     recipe.save()