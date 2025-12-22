from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import *
# Create your models here.

class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=200, null=True, blank=True)
    last_name = models.CharField(max_length=150, null=True, blank=True)
    is_varified = models.BooleanField(default=False)
    otp = models.CharField(max_length=6, null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    objects = UserManager()

    def __str__(self):
        return self.email

class Category(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='media/')

    def __str__(self):
        return self.name

class Recipe(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='media/')
   
    def __str__(self):
        return self.title
    
class RecipeType(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, null=True,blank=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
class RecipeVariant(models.Model):
    SIZE_VARIANT = (
        ('small','small'),
        ('medium', 'medium'),
        ('large', 'large')

    )
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,related_name='variants', null=True, blank=True)
    recipetype = models.ForeignKey(RecipeType, blank=True, on_delete=models.CASCADE)
    size = models.CharField(max_length=10, choices=SIZE_VARIANT)
    price = models.IntegerField(default=0)
    is_veg = models.BooleanField(default=True)

    def __str__(self):
        return self.size

class Order(models.Model):
    ORDER_STATUS = (
        ('pending','pending'),
        ('paid','paid'),
        ('canceled','canceled')
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    address = models.ForeignKey('Address', on_delete=models.SET_NULL, blank=True, null=True)
    status = models.CharField(max_length=20, choices=ORDER_STATUS, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def get_total_price(self):
        total = 0
        orderitems= OrderItems.objects.filter(order=self.id)
        for item in orderitems:
            item_price = item.total_price()
            total +=item_price
        return total
    
    def __str__(self):
        return f"{self.user.first_name}"
    
class OrderItems(models.Model):

    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    recipevariant = models.ForeignKey(RecipeVariant, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)

    def total_price(self):
        return self.recipevariant.price * self.quantity
    
    def __str__(self):
        return f"{self.quantity} -- {self.recipevariant}"
    
class Payment(models.Model):
    STATUS_CHOISE = (
        ('create','create'),
        ('success','success'),
        ('failed', 'failed')
    )
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    razorpay_order_id = models.CharField(max_length=100)
    razorpay_payment_id = models.CharField(max_length=100, null=True, blank=True)
    razorpay_signature = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOISE, default='create')
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"payment for order {self.order.id}"
    
class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=150)
    pincode = models.CharField(max_length=10, null=True, blank=True)
    phone = models.CharField(max_length=15)
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name 