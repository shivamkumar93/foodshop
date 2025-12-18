from django.contrib.auth.models import User
from .models import *
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate, get_user_model

# register serializer
class UserRegisterSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ['email', 'password','first_name','last_name', 'is_varified']
        extra_kwargs = {'password':{'write_only':True}}

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

# class ForgotPassword(serializers.Serializer):
#     email = serializers.EmailField()
#     class Meta:
#         fields = ['email']
                
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"

class RecipeSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    class Meta:
        model = Recipe
        fields = ['id','title','image','price','is_veg','category']

class OrderItemSerializer(serializers.Serializer):
    recipe_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value = 1)
    
    