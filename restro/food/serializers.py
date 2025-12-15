from django.contrib.auth.models import User
from .models import *
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only = True, validators = [validate_password])
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
    
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
             
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"

class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = "__all__"
    
    