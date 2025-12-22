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
    
    class Meta:
        model = Recipe
        fields = ['id','title','image','category']

class OrderItemSerializer(serializers.Serializer):
    recipevariant_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value = 1)
    
class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"
        read_only_fields = ['status', 'razorpay_payment_id', 'razorpay_signature']

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = "__all__"
        read_only_fields = ['user']

class RecipeVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeVariant
        fields = "__all__"
       

class RecipeTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeType
        fields = "__all__"